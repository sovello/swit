from sb.healthworker.datasets import _ngo_import
from sb.healthworker.models import NGORegistration

def run():
  _ngo_import.import_ngo_list('helpage_13Sept2013.csv', 'HelpAge', 1)

if __name__ == '__main__':
  run()


