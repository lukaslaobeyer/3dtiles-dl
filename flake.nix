{
  description = "Maps 3d tiles";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/master";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs { inherit system; };
      in {
        # packages.default = (pkgs.callPackage ./default.nix { });
        devShells.default = (import ./shell.nix { inherit pkgs; });
      });

  nixConfig = {
    bash-prompt = "\[3dtiles:\\w\]$ ";
  };
}
