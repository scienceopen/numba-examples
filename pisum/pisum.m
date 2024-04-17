function pisum(N, Nrun)

addpath('..')  % isoctave

print_version()

pitry = calc_pisum(N);

if abs(pitry-pi)>1e-4
  error('Pisum: failed to converge')
end

f = @() calc_pisum(N);

t = bench_time(f, Nrun);

disp([num2str(t),' sec.'])

end % function pisum
%%
function x = calc_pisum(N)
s = 0.;
for k = 1:N
  s = s + (-1)^(k+1) / (2*k-1);
end

x=4*s;
end
