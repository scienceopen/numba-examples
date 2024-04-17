% like iter.f90
Nrun = 10;
N = 100000;

addpath('..')

A = rand(N,1);

f = @() simple_iter(A);

t = bench_time(f, Nrun);

disp([num2str(t),' sec.'])

%%
function x = simple_iter(A) %must return at least one argument or timeit breaks
  x=0;
  for i = A
    x = 0.5*x + mod(i, 10);
    if x>1e100; break; end
  end
end
