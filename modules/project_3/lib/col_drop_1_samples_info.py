class ColDrop1SamplesInfo(object):
    def __init__(self, filename_template='cd1_sample{}_s4400.p',
                 dirname='col_drop_1_samples', p3_dir_loc='assets',
                 file_count=50, start_index=1, index_format='%d',
                 sample_size = 4400):
        self.filename_template = filename_template
        self.dirname = dirname
        self.p3_dir_loc = p3_dir_loc
        self.file_count = file_count
        self.start_index = start_index
        self.index_format = index_format
        self.sample_size = sample_size
    

    @property
    def p3_filename_template(self):
        return '/'.join([self.p3_dir_loc, self.dirname,
                         self.filename_template])



    def format_filename(self, format_val, path_in_p3=True):
        if path_in_p3 == True:
            filename = self.p3_filename_template
        else:
            filename = self.filename_template
        return filename.format(format_val)



    def format_fname_list(self, first=1, last=-1, step=1, path_in_p3=True):
        return [self.format_filename(self.format_index(i), path_in_p3)
                for i in self.index_list(first, last, step)]



    def index_list(self, first=1, last=-1, step=1):
        if step < 0:
            last += first
            first = last - first
            last -= first
            step *= -1
        first = self.fortify_index(first - bool(first))
        last = self.fortify_index(last)
        return list(range(first, last, step))



    def fortify_index(self, index):
        if index < self.file_count:
            if index < 0:
                if  -index <= self.file_count:
                    index += self.file_count + 1
                else:
                    index = 0
            return index + self.start_index
        return self.start_index + self.file_count + 1



    def format_index(self, index):
        if not self.index_format:
            return str()

        c, *self.index_format = self.index_format

        if not self.index_format:
            format_str = str()
        elif c != '\\' and c != '%':
            format_str = c
        else:
            c += self.index_format.pop(0)
            if c[0] == '\\':
                format_str = c[1]
            else:
                while self.index_format and not c[-1].isalpha():
                    c += self.index_format.pop(0)
                format_str = '{1:{0}}'.format(c[1:], index)

        format_str += self.format_index(index)
        self.index_format = c + ''.join(self.index_format)
        return format_str
