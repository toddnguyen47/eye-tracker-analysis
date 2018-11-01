# import EMDAT_src
import core.fixations as fixations
import params


if __name__ == "__main__":
    fixations.read_in_csv(params.INPUT_CSV_FILENAME)
