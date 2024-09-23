py_library(
    name = "matching-theory",
    srcs = [
        "matching_theory.py",
    ],
    visibility = ["//visibility:public"]
)

py_test(
    name = "test_matching_theory",
    srcs = ["test_matching_theory.py"],
    deps = [
        ":matching-theory",
    ],
)

filegroup(
    name = "srcs",
    srcs = ["BUILD"] + glob(["**/*.py"]),
    visibility = ["//visibility:public"],
)