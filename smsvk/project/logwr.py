import logging


def log_wr(api_log_file,level_):
    
    logging.basicConfig(
		filename=api_log_file, 
		filemode="w", 
		format='[%(asctime)s] - [%(levelname)s] => %(message)s',
  		level=level_
	)
