% iterative dor product with a for loope

function retval = dotProductIterative (A, B)
	if size(A,1) ~= size(B,1),
		error ('expecting same size, 1d vectors');
	endif;

	if (size(A,2) ~= 1) || (size(B,2) ~= 1),
		error ('expecting 1d vectors') 
	endif;

	retval = 0.0;
	for i=1:size(A,1),
		retval = retval + A(i, 1) * B(i, 1);
	end;
endfunction;