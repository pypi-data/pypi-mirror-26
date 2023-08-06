export PyMetrology_source_path=${PWD}
export PyMetrology_examples_path=${PyMetrology_source_path}/examples

source /opt/python-virtual-env/py35/bin/activate
append_to_python_path_if_not ${PyMetrology_source_path}
append_to_python_path_if_not ${PyMetrology_source_path}/tools
