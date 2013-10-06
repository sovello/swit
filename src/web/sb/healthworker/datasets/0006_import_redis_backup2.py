from sb.healthworker.datasets import _redis_import
from sb.healthworker.datasets import _helpers

def run():
  _redis_import.import_redis_backup(_helpers.get_path('kv-backup-20131005.json'))

if __name__ == '__main__':
  run()

