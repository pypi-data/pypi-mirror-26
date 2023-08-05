# coding=utf-8
import stat
import os
from abc import ABCMeta, abstractmethod


class TreeCache:
    __metaclass__ = ABCMeta

    @classmethod
    def _files_sha_array_to_dict(cls, files):
        result = {}
        for file_with_sha_mode in files.split(b'\n'):
            name, sha, mode = file_with_sha_mode.split(b'|')
            result[name] = (sha, int(mode))

        return result

    @classmethod
    def _folders_to_scan(cls, entries):
        scan_path = {b'': [True, set()]}

        for name, entry in entries.items():
            ctime, mtime, dev, ino, mode, uid, gid, size, sha, flags = entry

            dir_name = os.path.dirname(name)

            scan_path.setdefault(dir_name, [True, set()])[1].add((os.path.basename(name), sha, mode))

            dir_parts = [b''] + dir_name.split(b'/')
            for _ in dir_parts[:-1]:
                current_dir = os.path.join(*dir_parts[:-1])
                dir_scan_info = scan_path.setdefault(current_dir, [False, set()])
                dir_scan_info[0] = False
                dir_scan_info[1].add((dir_parts[-1], None, stat.S_IFDIR))

                dir_parts.pop()

        for path, should_scan_files in scan_path.items():
            yield path, should_scan_files[0], should_scan_files[1]

    @classmethod
    def __combine_files_with(cls, scans, current_data):
        for path, should_scan, files_with_sha in scans:
            for file_name, sha, mode in files_with_sha:
                current_data.setdefault(path, {})[file_name] = (sha, mode)

    @classmethod
    def _path_split(cls, current_path):
        try:
            dir_name, base_name = current_path.rsplit(b'/', 1)
        except ValueError:
            return b'', current_path
        else:
            return dir_name, base_name

    @classmethod
    def __build_tree_structure(cls, current_data):
        trees = {}

        def add_tree(current_path):
            prev_current_path = trees.get(current_path)

            if prev_current_path is not None:
                return prev_current_path

            dir_name, base_name = cls._path_split(current_path)

            if base_name:
                t = add_tree(dir_name).setdefault(base_name, {})
            else:
                t = trees.setdefault(current_path, {})

            return t

        for path, files in current_data.items():
            for base_name, sha_and_mode in files.items():
                current_sha, current_mode = sha_and_mode

                if current_mode & stat.S_IFDIR:
                    add_tree(base_name)
                else:
                    _, base_name_file_name = cls._path_split(base_name)
                    tree = add_tree(path)
                    tree[base_name_file_name] = (current_mode, current_sha)

        return trees

    @classmethod
    def make_bytes(cls, c):
        return c if isinstance(c, bytes) else c.encode('utf-8')

    @classmethod
    def __build_sha_tree(cls, current_data, root):
        from ...dulwich.objects import Tree

        current_tree = Tree()
        for child, sha_with_mode in current_data[root].items():
            sha, mode = sha_with_mode

            is_root = len(child) == 0

            if not is_root:
                if sha is None:
                    child_tree = cls.__build_sha_tree(current_data, child)
                    sha = child_tree.id
                    current_data[root][child] = child_tree

                current_tree.add(cls.make_bytes(child), mode, cls.make_bytes(sha))

        current_data[root] = current_tree
        return current_tree

    def set_entries(self, entries):
        scans = list(self._folders_to_scan(entries))

        current_data = self._get_files(scans)

        self.__combine_files_with(scans, current_data)

        self.__build_sha_tree(current_data, b'')

        self._set_files(current_data)

    @classmethod
    def build_blob(cls, tree):
        for item in tree.iteritems():
            yield '|'.join([item.path.decode('utf8'), item.sha.decode('utf8'), str(item.mode)])

    @abstractmethod
    def _get_files(self, scans):
        raise NotImplemented(self._get_files)

    @abstractmethod
    def _set_files(self, trees_objects):
        raise NotImplemented(self._set_files)

    @abstractmethod
    def get_commit_id(self):
        raise NotImplemented(self._set_files)
