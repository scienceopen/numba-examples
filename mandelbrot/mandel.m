
%% mandelbrot
%mandel(complex(-.53,.68));
%assert(sum(sum(mandelperf(true))) == 14791)

Nrun = 1;

addpath("..")

f = @() mandelperf();

t = bench_time(f, Nrun);

disp([num2str(t),' sec.'])

%%
function n = mandel1(z)
  c = z;
  for n=0:79
    if abs(z)>2
      return
    end
    z = z^2+c;
  end
  n = 80;
end
%%
function M = mandelperf(~)
  x=-2.0:.1:0.5;
  y=-1:.1:1;
  M=zeros(length(y),length(x));
  for r=1:size(M,1)
    for c=1:size(M,2)
     M(r,c) = mandel1(x(c)+y(r)*1j);
    end
  end
end
