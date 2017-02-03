% Vectorized dot product

function retval = dotProduct (A, B)

	if size(A,1) ~= size(B,1),
		error ('expecting same size, 1d vectors');
	endif;

	if (size(A,2) ~= 1) || (size(B,2) ~= 1),
		error ('expecting 1d vectors') 
	endif;
	retval = transpose(A) * B;
endfunction