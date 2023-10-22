#!/usr/bin/env perl

use v5.30;
use strict;
use warnings;
no warnings 'experimental::signatures';
use feature 'signatures';
use autodie;

use FindBin qw( $Bin );
use File::Spec;
use lib File::Spec->catdir( $Bin, 'lib' );

use Getopt::Long;
use IPC::System::Simple qw( capturex );
use Path::Tiny          qw( path );
use Test::More;

sub main {
    my $target;
    my $expect_cross;
    my $expect_cross_version;
    my $expect_file_re;
    my $expect_stripped;

    GetOptions(
        'target=s'               => \$target,
        'expect-file-re=s'       => \$expect_file_re,
        'expect-cross!'          => \$expect_cross,
        'expect-cross-version=s' => \$expect_cross_version,
        'expect-stripped!'       => \$expect_stripped,
    );

    check_cross(
        path( $ENV{RUNNER_TEMP} ), $expect_cross,
        $expect_cross_version
    );

    for my $bin (
        path( qw( . target ),          $target, qw( debug test-project ) ),
        path( qw( . subcrate target ), $target, qw( debug subcrate ) )
    ) {
        check_binary( $bin, $expect_file_re, $expect_stripped );
    }

    done_testing();
}

sub check_cross ( $bin_dir, $expect_cross, $expect_cross_version ) {
    my $cross = $bin_dir->child('cross');
    if ($expect_cross) {
        ok( $cross->is_file && -x $cross, 'found `cross` in $PATH' );
        if ($expect_cross_version) {
            my $version = capturex( $cross, '--version' );
            like(
                $version, qr/\Q$expect_cross_version/,
                'cross version matches expected version'
            );
        }
    }
    else {
        ok( !$cross->exists, 'did not find `cross` in $PATH' );
    }
}

sub check_binary ( $bin, $expect_file_re, $expect_stripped ) {
    ok( $bin->exists, "Binary at $bin exists" )
        or return;
    ok( $bin->is_file, "Binary at $bin is a file" )
        or return;
    ok( -x $bin, "Binary at $bin is executable" )
        or return;

    my $file = capturex( qw( file --brief ), $bin ) // q{};
    chomp $file;

    like(
        $file, qr/$expect_file_re/,
        "`file` output for $bin matches expected output"
    );

    # The file command on macOS doesn't report whether the binary is stripped
    # or not.
    return if $^O eq 'darwin';

    if ($expect_stripped) {
        unlike(
            $file, qr/not stripped/,
            "`file` does not report $bin as not stripped"
        );
        like( $file, qr/stripped/, "`file` reports $bin as stripped" );
    }
    else {
        if ( $^O eq 'MSWin32' || $^O eq 'msys' ) {

            # On Windows, unstripped binaries don't contain the word
            # "stripped" at all.
            unlike(
                $file, qr/stripped/,
                "`file` does not report $bin as stripped"
            );
        }
        else {
            like(
                $file, qr/not stripped/,
                "`file` reports $bin as not stripped"
            );
        }
    }
}

main();
