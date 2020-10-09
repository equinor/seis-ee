from segdpy import segdpy


def number_of_samples_in_segd_file(file_path: str) -> int:
    segdfile = segdpy.SegDFile(file_path)
    return segdfile.segdrecord.samples_per_trace


if __name__ == '__main__':
    number_of_samples_in_segd_file("../../test_data/grane/full-files/segd-test.sgd")
