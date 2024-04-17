function matmul(N, Nrun)

addpath('..')  % isoctave

print_version()

A = randn(N,N);
B = randn(N,N);
f = @() A*B;

t = bench_time(f, Nrun);

disp([num2str(t),' seconds for N=',int2str(N)])

end % function
