% iterative dor product with a for loop, returning two values

function [retval, length] = dotProductIterativeDret (A, B)
	if size(A,1) ~= size(B,1),
		error ('expecting same size, 1d vectors');
	endif;

	if (size(A,2) ~= 1) || (size(B,2) ~= 1),
		error ('expecting 1d vectors') 
	endif;

	retval = 0.0;
	maxlength = 1000;
	length = size(A,1)
	for i=1:maxlength,
		retval = retval + A(i, 1) * B(i, 1);

		if (i == length),
			break;
		end;
	end;
endfunction;