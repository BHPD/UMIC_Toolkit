# -*- coding: utf-8 -*-
"""
GUI wrapper around biomero-converter (https://github.com/NL-BioImaging/biomero-converter).

Converts microscopy files (Leica, Incucyte, iSyntax, MIRAX, DICOM, .db, (OME-)TIFF,
OME-Zarr, ...) to OME-Zarr or OME-TIFF. All conversion logic lives in the
biomero-converter package; this module only provides the interface.
"""

import customtkinter, threading, queue, logging, json, os
from tkinter import filedialog

# Imported here so a missing package raises ImportError when the module is opened,
# which main.py turns into a friendly message instead of a crash.
from biomero_converter.converter import convert

try:
    from importlib.metadata import version as _pkg_version
    CONVERTER_VERSION = _pkg_version('biomero-converter')
except Exception:
    CONVERTER_VERSION = 'unknown'

OUTPUT_FORMATS = {
    'OME-Zarr v0.4': 'omezarr04',
    'OME-Zarr v0.5': 'omezarr05',
    'OME-Zarr v0.6': 'omezarr06',
    'OME-TIFF': 'ometiff',
}

INPUT_FILETYPES = [
    ('Supported files', '*.lif *.lof *.lifext *.xlif *.xlcf *.xlef *.icarch *.isyntax *.mrxs '
                        '*.db *.dcm *.dicom *.tif *.tiff *.ome *.xml'),
    ('Leica', '*.lif *.lof *.lifext *.xlif *.xlcf *.xlef'),
    ('Incucyte archive', '*.icarch'),
    ('Whole slide (iSyntax, MIRAX)', '*.isyntax *.mrxs'),
    ('DICOM', '*.dcm *.dicom'),
    ('TIFF / OME-TIFF', '*.tif *.tiff'),
    ('All files', '*.*'),
]


class _QueueLogHandler(logging.Handler):
    """Forwards log records from the worker thread to the GUI thread."""

    def __init__(self, q):
        super().__init__(level=logging.INFO)
        self.q = q
        self.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s', '%H:%M:%S'))

    def filter(self, record):
        # Show INFO from biomero-converter itself (it logs to the root logger),
        # but only warnings/errors from its dependencies (linkml, ome_zarr, ...).
        return (record.levelno >= logging.WARNING
                or record.name == 'root' or record.name.startswith('biomero_converter'))

    def emit(self, record):
        try:
            self.q.put(('log', self.format(record)))
        except Exception:
            self.handleError(record)


class BiomeroConverter(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        # Standard GUI parameters
        self.title(f'biomero-converter {CONVERTER_VERSION}')
        self.geometry("960x640")
        self.transient(master)
        self.lift()
        self.focus_force()

        # State
        self.inputs = []                  # list of input paths (files or folders)
        self.output_folder = None
        self.msg_queue = queue.Queue()    # worker -> GUI messages
        self.worker = None
        self.stop_requested = threading.Event()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # Row 0, info text
        customtkinter.CTkLabel(
            self,
            text='Convert microscopy files to OME-Zarr or OME-TIFF using biomero-converter.'
                 '\nSupports Leica, Incucyte, iSyntax, MIRAX, DICOM, image .db, (OME-)TIFF and OME-Zarr.',
            anchor='center').grid(row=0, column=0, sticky='new', pady=5, padx=10)

        # Row 1, input list + buttons
        input_frame = customtkinter.CTkFrame(self)
        input_frame.grid(row=1, column=0, sticky='nsew', pady=5, padx=10)
        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_rowconfigure(1, weight=1)

        customtkinter.CTkLabel(input_frame, text='Input files / folders', anchor='w').grid(
            row=0, column=0, sticky='w', pady=(5, 0), padx=5)
        self.input_box = customtkinter.CTkTextbox(input_frame, height=120, wrap='none')
        self.input_box.grid(row=1, column=0, rowspan=4, sticky='nsew', pady=5, padx=5)
        self.input_box.configure(state='disabled')

        self.add_files_btn = customtkinter.CTkButton(input_frame, text='Add files', command=self.add_files)
        self.add_files_btn.grid(row=1, column=1, sticky='ew', pady=5, padx=5)
        self.add_folder_btn = customtkinter.CTkButton(
            input_frame, text='Add folder', command=self.add_folder)
        self.add_folder_btn.grid(row=2, column=1, sticky='ew', pady=5, padx=5)
        self.clear_btn = customtkinter.CTkButton(input_frame, text='Clear', command=self.clear_inputs)
        self.clear_btn.grid(row=3, column=1, sticky='ew', pady=5, padx=5)

        # Row 2, output folder
        output_frame = customtkinter.CTkFrame(self)
        output_frame.grid(row=2, column=0, sticky='ew', pady=5, padx=10)
        output_frame.grid_columnconfigure(0, weight=1)
        self.output_label = customtkinter.CTkLabel(output_frame, text='Output folder: (none selected)', anchor='w')
        self.output_label.grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.output_btn = customtkinter.CTkButton(output_frame, text='Browse', command=self.browse_output)
        self.output_btn.grid(row=0, column=1, sticky='ew', pady=5, padx=5)

        # Row 3, options
        options = customtkinter.CTkFrame(self)
        options.grid(row=3, column=0, sticky='ew', pady=5, padx=10)
        options.grid_columnconfigure((1, 3, 5), weight=1)

        customtkinter.CTkLabel(options, text='Output format:', anchor='w').grid(
            row=0, column=0, sticky='w', pady=5, padx=5)
        self.format_menu = customtkinter.CTkOptionMenu(options, values=list(OUTPUT_FORMATS))
        self.format_menu.set('OME-Zarr v0.4')
        self.format_menu.grid(row=0, column=1, sticky='ew', pady=5, padx=5)

        customtkinter.CTkLabel(options, text='Incucyte plate ID:', anchor='w').grid(
            row=0, column=2, sticky='w', pady=5, padx=5)
        self.plate_entry = customtkinter.CTkEntry(options, placeholder_text='all plates')
        self.plate_entry.grid(row=0, column=3, sticky='ew', pady=5, padx=5)

        customtkinter.CTkLabel(options, text='Leica image UUID:', anchor='w').grid(
            row=0, column=4, sticky='w', pady=5, padx=5)
        self.uuid_entry = customtkinter.CTkEntry(options, placeholder_text='all images')
        self.uuid_entry.grid(row=0, column=5, sticky='ew', pady=5, padx=5)

        # Row 4, log
        self.log_box = customtkinter.CTkTextbox(self, wrap='word')
        self.log_box.grid(row=4, column=0, sticky='nsew', pady=5, padx=10)
        self.log_box.configure(state='disabled')

        # Row 5, progress + run/stop
        run_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        run_frame.grid(row=5, column=0, sticky='ew', pady=(5, 10), padx=10)
        run_frame.grid_columnconfigure(0, weight=1)
        self.progress = customtkinter.CTkProgressBar(run_frame)
        self.progress.set(0)
        self.progress.grid(row=0, column=0, sticky='ew', pady=5, padx=5)
        self.stop_btn = customtkinter.CTkButton(
            run_frame, text='Stop after current', state='disabled', command=self.request_stop)
        self.stop_btn.grid(row=0, column=1, sticky='e', pady=5, padx=5)
        self.convert_btn = customtkinter.CTkButton(run_frame, text='Convert', command=self.start_conversion)
        self.convert_btn.grid(row=0, column=2, sticky='e', pady=5, padx=5)

        self.protocol('WM_DELETE_WINDOW', self.on_close)

    # ---------- Input / output selection ----------
    def add_files(self):
        paths = filedialog.askopenfilenames(parent=self, title='Select input files', filetypes=INPUT_FILETYPES)
        self._add_inputs(paths)

    def add_folder(self):
        # For folder-based inputs, e.g. OME-Zarr (.zarr directories) or DICOM folders
        path = filedialog.askdirectory(parent=self, title='Select input folder (OME-Zarr, DICOM, ...)')
        if path:
            self._add_inputs([path])

    def _add_inputs(self, paths):
        for p in paths:
            p = os.path.normpath(p)
            if p not in self.inputs:
                self.inputs.append(p)
        self._refresh_inputs()

    def clear_inputs(self):
        self.inputs = []
        self._refresh_inputs()

    def _refresh_inputs(self):
        self.input_box.configure(state='normal')
        self.input_box.delete('0.0', 'end')
        self.input_box.insert('0.0', '\n'.join(self.inputs))
        self.input_box.configure(state='disabled')

    def browse_output(self):
        path = filedialog.askdirectory(parent=self, title='Select output folder')
        if path:
            self.output_folder = os.path.normpath(path)
            self.output_label.configure(text=f'Output folder: {self.output_folder}')

    # ---------- Logging ----------
    def log(self, text):
        self.log_box.configure(state='normal')
        self.log_box.insert('end', text + '\n')
        self.log_box.see('end')
        self.log_box.configure(state='disabled')

    # ---------- Conversion ----------
    def start_conversion(self):
        if not self.inputs:
            self.log('Please add at least one input file or folder.')
            return
        if not self.output_folder:
            self.log('Please select an output folder.')
            return

        kwargs = {}
        plate_id = self.plate_entry.get().strip()
        image_uuid = self.uuid_entry.get().strip()
        if plate_id:
            kwargs['plate_id'] = plate_id
        if image_uuid:
            kwargs['image_uuid'] = image_uuid

        job = dict(
            inputs=list(self.inputs),
            output_folder=self.output_folder,
            output_format=OUTPUT_FORMATS[self.format_menu.get()],
            kwargs=kwargs,
        )

        self.stop_requested.clear()
        self._set_running(True)
        self.progress.set(0)
        self.worker = threading.Thread(target=self._worker, args=(job,), daemon=True)
        self.worker.start()
        self.after(100, self._poll_queue)

    def request_stop(self):
        self.stop_requested.set()
        self.stop_btn.configure(state='disabled')
        self.log('Stop requested: finishing the current file, then stopping.')

    def _worker(self, job):
        q = self.msg_queue
        handler = _QueueLogHandler(q)
        root_logger = logging.getLogger()
        old_level = root_logger.level
        root_logger.addHandler(handler)
        root_logger.setLevel(logging.INFO)
        logging.getLogger('ome_zarr').setLevel(logging.WARNING)

        n = len(job['inputs'])
        n_ok = 0
        try:
            for i, path in enumerate(job['inputs']):
                if self.stop_requested.is_set():
                    q.put(('log', 'Stopped by user.'))
                    break
                q.put(('log', f'[{i + 1}/{n}] Converting {path}'))
                try:
                    result = convert(path, job['output_folder'],
                                     output_format=job['output_format'],
                                     **job['kwargs'])
                    for item in json.loads(result or '[]'):
                        q.put(('log', f"    -> {item.get('full_path', item)}"))
                    n_ok += 1
                except Exception as e:
                    # The underlying cause is already logged by biomero-converter (ERROR line above)
                    q.put(('log', f'    FAILED: {e}'))
                q.put(('progress', (i + 1) / n))
        finally:
            root_logger.removeHandler(handler)
            root_logger.setLevel(old_level)
            q.put(('done', f'Finished: {n_ok}/{n} input(s) converted successfully.'))

    def _poll_queue(self):
        done = False
        try:
            while True:
                kind, payload = self.msg_queue.get_nowait()
                if kind == 'log':
                    self.log(payload)
                elif kind == 'progress':
                    self.progress.set(payload)
                elif kind == 'done':
                    self.log(payload)
                    done = True
        except queue.Empty:
            pass
        if done:
            self._set_running(False)
        elif self.winfo_exists():
            self.after(100, self._poll_queue)

    def _set_running(self, running):
        state = 'disabled' if running else 'normal'
        for w in (self.convert_btn, self.add_files_btn, self.add_folder_btn, self.clear_btn,
                  self.output_btn, self.format_menu, self.plate_entry, self.uuid_entry):
            w.configure(state=state)
        self.stop_btn.configure(state='normal' if running else 'disabled')

    def on_close(self):
        if self.worker is not None and self.worker.is_alive():
            self.stop_requested.set()
            self.log('A conversion is still running; it will stop after the current file.')
            return
        self.destroy()
