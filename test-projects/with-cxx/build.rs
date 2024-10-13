fn main() {
    cxx_build::bridge("src/main.rs")
        .file("src/blobstore.cc")
        .std("c++14")
        .compile("cxxbridge-demo");

    println!("cargo:rerun-if-changed=src/main.rs");
    println!("cargo:rerun-if-changed=src/blobstore.cc");
    println!("cargo:rerun-if-changed=include/blobstore.h");
    println!("cargo:rustc-link-search=/home/autarch/tmp/musl/x86_64-multilib-linux-musl/x86_64-multilib-linux-musl/sysroot/lib");
    println!("cargo:rustc-link-lib=static=stdc++");
}
