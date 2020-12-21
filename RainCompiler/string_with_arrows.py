def string_with_arrows(text, position_start, position_end):
	result = ''

	# Calculate indices
	index_start = max(text.rfind('\n', 0, position_start.idx), 0)
	index_end = text.find('\n', index_start + 1)
	if index_end < 0: index_end = len(text)
	
	# Generate each line
	line_count = position_end.ln - position_start.ln + 1
	for i in range(line_count):
		# Calculate line columns
		line = text[index_start:index_end]
		col_start = position_start.col if i == 0 else 0
		col_end = position_end.col if i == line_count - 1 else len(line) - 1

		# Append to result
		result += line + '\n'
		result += ' ' * col_start + '^' * (col_end - col_start)

		# Re-calculate indices
		index_start = index_end
		index_end = text.find('\n', index_start + 1)
		if index_end < 0: index_end = len(text)

	return result.replace('\t', '')
