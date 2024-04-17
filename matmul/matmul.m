function matmul(N, Nrun)

addpath('..')  % isoctave

print_version()

A = randn(N,N);
B = randn(N,N);
f = @() A*B;

try % matlab
tcum = timeit(f);
catch % octave
tcum = inf;
for i=1:Nrun
  tic
  f();
  tcum=min(tcum,toc);
end
end % try
disp([num2str(tcum),' seconds for N=',int2str(N)])

end % function
