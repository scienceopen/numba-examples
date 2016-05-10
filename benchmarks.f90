program benchmarks

    use, intrinsic :: iso_fortran_env, only : sp=>REAL32,dp=>REAL64, INT64, stderr=>error_unit

    use benchmark_matmul,only: double_matmul,single_matmul
    use benchmark_iter,only : simple_iter,mandeltest
    use benchmark_hypot,only: benchhypot

    Implicit None

    integer,parameter :: Nmatmul=5000, Nrunmatmul=10, Nmand=5
    integer,parameter :: Niter=1000000, Nruniter=100,Nrunmand=1000

    real(dp) :: tdmatmul,tsmatmul,titer,tmandel,Rhypot

!----- tests-----------
    tdmatmul = double_matmul(Nmatmul,Nrunmatmul)
    tsmatmul = single_matmul(Nmatmul,Nrunmatmul)

    titer = simple_iter(Niter,Nruniter)
!------mandlebrot-------------
    tmandel=mandeltest(Nmand,Nrunmand)
!------ hypot -----------------
     Rhypot = benchhypot()

    write(stderr,*) tdmatmul,tsmatmul,titer,tmandel
    print *, 'sqrt(a^2+b^2) / hypot(a,b)  time ratio (hypot is slower): ',Rhypot

end program

