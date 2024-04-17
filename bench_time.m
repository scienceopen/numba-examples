function t = bench_time(f, Nrun)

try % matlab
  t = timeit(f);
catch % octave
  t = inf;
  for i=1:Nrun
    tic
    f();
    t = min(t, toc);
  end

end % try
