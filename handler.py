import fnmatch
import os
import re

import inference

PRE_DIR = 'test_dir/input/pre'
POST_DIR = 'test_dir/input/post'
OUTPUT_DIR = 'test_dir/output'


class Files(object):

    def __init__(self, pre, post):
        self.pre = os.path.abspath(os.path.join(PRE_DIR, pre))
        self.post = os.path.abspath(os.path.join(POST_DIR, post))
        self.base_num = self.check_base_num()
        self.output_loc = os.path.abspath(os.path.join(OUTPUT_DIR, 'loc', f'{self.base_num}_loc.png'))
        self.output_dmg = os.path.abspath(os.path.join(OUTPUT_DIR, 'dmg', f'{self.base_num}_dmg.png'))

    def check_base_num(self):
        """
        Checks that the number sequence matches for both the pre and post images. This should ensure the pre and post
        images cover the same extent.
        :return: True if numbers match
        """
        pre_base = ''.join([digit for digit in self.pre if digit.isdigit()])
        post_base = ''.join([digit for digit in self.post if digit.isdigit()])
        if pre_base == post_base:
            return pre_base

    def infer(self):
        """
        Passes object to inference.
        :return: True if successful
        """

        self.opts = inference.Options(self.pre, self.post, self.output_loc, self.output_dmg),

        try:
            # TODO: Not sure why opts seems to be a list.
            inference.main(self.opts[0])
        except Exception as e:
            print(f'File: {self.pre}. Error: {e}')
            return False

        return True

    def georef(self):
        pass


def main():

    pre_files = sorted(get_files(PRE_DIR))
    post_files = sorted(get_files(POST_DIR))
    string_len_check(pre_files, post_files)
    file_objs = []
    for pre, post in zip(pre_files, post_files):
        file_objs.append(Files(pre, post))

    for obj in file_objs:
        obj.infer()

def make_output_structure(path):
    pass


def get_files(where, which='*.png'):
    """
    Gathers list of files from path
    :param where: Path to search
    :param which: string to match (default: *.png)
    :return: List of files in path matching rule
    """

    rule = re.compile(fnmatch.translate(which), re.IGNORECASE)
    return [name for name in os.listdir(where) if rule.match(name)]


def string_len_check(pre, post):

    if len(pre) != len(post):
        # TODO: Add some helpful info on why this failed
        return False

    return True


if __name__ == '__main__':
    main()