function print_version()

if isoctave
  v = ver('octave'); % else matlab syntax checker errors
  disp(['--> Octave ', v.Version])
else
  disp("--> Matlab " + matlabRelease.Release)
end

end
