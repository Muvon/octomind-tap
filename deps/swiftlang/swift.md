# swiftlang/swift

The Swift toolchain — compiler (`swiftc`), REPL, and the Swift Package Manager (`swift package`, `swift build`, `swift test`). On macOS it ships with the Xcode Command Line Tools; on Linux it is installed via swiftly, the official swift.org toolchain manager.

## Key Commands

| Command | Description |
|---------|-------------|
| `swift build` | Build a Swift package |
| `swift test` | Run package tests |
| `swift run` | Build and run an executable target |
| `swift package init` | Scaffold a new package |
| `swiftc file.swift` | Compile a single file |

## Common Usage

```bash
# Build and test a package
swift build
swift test

# Run an executable target
swift run my-tool --flag

# Check toolchain version
swift --version
```

## Links

- [Homepage](https://www.swift.org)
- [Documentation](https://www.swift.org/documentation/)
