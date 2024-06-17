package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "auto-push",
	Short: "A CLI tool to update your GitHub profile",
	Long: `Auto-push is a CLI tool that helps you easily update your GitHub profile status with a custom message and emoji.
	
Examples:
  auto-push profile --name "John Doe" --bio "Software Engineer"
  auto-push status --message "Working from home" --emoji ":house_with_garden:"
  auto-push status -m "In a meeting" -e ":speech_balloon:"`,
}

func Execute() {
	rootCmd.CompletionOptions.DisableDefaultCmd = true
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
