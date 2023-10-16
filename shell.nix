{ pkgs, ... }:
let
  pythonPkgs = pkgs.python311Packages;
  pythonWithPkgs = pythonPkgs.python.withPackages (p: with p; [
    numpy
    requests
    tqdm
  ]);
in
pkgs.stdenvNoCC.mkDerivation rec {
  name = "3dtiles-shell";
  nativeBuildInputs = [
    pythonWithPkgs
  ];
}
