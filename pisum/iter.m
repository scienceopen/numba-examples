function iter()

if isoctave
    disp('--> Octave')
else
    disp('--> Matlab')
end

%% simple_iter
  printf('simple_iter ')
  A = rand(1000000,1);
  f = @() simple_iter(A); % this anon function required by timeit
  try
    timeit(f)
  catch
    tic
    simple_iter(A);
    t = toc;
    disp([num2str(t),' sec.'])
  end
%% mandelbrot
%mandel(complex(-.53,.68));
%assert(sum(sum(mandelperf(true))) == 14791)

printf('mandelbrot ')
  try
    f = @() mandelperf(false);
    timeit(f)
  catch
    tic
    mandelperf();
    t = toc;
    disp([num2str(t),' sec.'])
  end

end

function x= simple_iter(A) %must return at least one argument or timeit breaks
 x=0;
    for i = A
        x = 0.5*x + mod(i, 10);
    end
end
%----------------------------
function n = mandel(z)
    c = z;
    for n=0:79
        if abs(z)>2
            return
        end
        z = z^2+c;
    end
    n = 80;
end

function M = mandelperf(~)
    x=-2.0:.1:0.5;
    y=-1:.1:1;
    M=zeros(length(y),length(x));
    for r=1:size(M,1)
        for c=1:size(M,2)
           M(r,c) = mandel(x(c)+y(r)*1j);
        end
    end
end
%---------------------------------------------
