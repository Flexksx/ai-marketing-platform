{pkgs}: {
  packages = with pkgs; [
    jdk25
    gradle
  ];

  shellHook = ''
    export JAVA_HOME="${pkgs.jdk25}"
  '';
}
