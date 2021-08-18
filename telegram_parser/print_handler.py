def print_func(parser_config, output):
    if parser_config['output_source'] == '1':
        print(output)
    else:
        parser_config['bot'].send_message(parser_config['user_id'],
                                          output)
