{
  description = "Camera Server - Local Network Camera Stream";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python312
            python312Packages.pip
            python312Packages.opencv4
            python312Packages.flask
            python312Packages.werkzeug
            python312Packages.jinja2
            v4l-utils
            ffmpeg
          ];

          shellHook = "\n            echo \"Camera Server Development Environment\"\n            echo \"======================================\"\n            echo \"Python: \$(python --version)\"\n            echo \"\"\n            echo \"Available commands:\"\n            echo \"  - nix develop      : Enter the development environment\"\n            echo \"  - python src/main.py: Start the camera server\"\n            echo \"\"\n          ";
        };
      }
    );
}
