
package cmd

import (
    "fmt"
    "os"

    "github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
    Use:   "github-cli",
    Short: "A CLI to update GitHub profile",
    Long:  `A Command Line Interface to update GitHub profile information such as name and bio.`,
}

func Execute() {
    if err := rootCmd.Execute(); err != nil {
        fmt.Println(err)
        os.Exit(1)
    }
}
