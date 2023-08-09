class Entry(object):
    def __init__(self, p_time, p_name, p_position, p_content, p_with_link, p_address, p_link_content):
        self.time = p_time
        self.name = p_name
        self.position = p_position
        self.content = p_content
        self.with_link = p_with_link
        self.address = p_address
        self.link_content = p_link_content

    def __str__(self):
        print(f'{self.time}, {self.name}, '
              f'{self.position}, {self.content}, '
              f'{self.with_link}, {self.address}, '
              f'{self.link_content}')


class DataModel(object):
    def __init__(self):
        self.entries = []

    def append(self, p_entry):
        self.entries.append(p_entry)


# 判断文件是否自身执行，如果是则，执行之后的语句
if __name__ == '__main__':
    pass