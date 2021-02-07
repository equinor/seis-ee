from segdpy.segdfile import SegDFile


def number_of_samples_in_segd_file(file_path: str) -> int:
    segdfile = SegDFile(file_path)
    return segdfile.segdrecord.samples_per_trace

