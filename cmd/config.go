package cmd

import (
	"fmt"
	"os"

	"github.com/fatih/color"
	"github.com/spf13/cobra"
)

var (
	token      string
	weatherKey string
)

var configCmd = &cobra.Command{
	Use:   "config",
	Short: "Configure environment variables",
	Run: func(cmd *cobra.Command, args []string) {
		if token == "" && weatherKey == "" {
			cmd.Help()
			return
		}

		if token != "" {
			err := os.Setenv("GITHUB_TOKEN", token)
			if err != nil {
				color.Red("Error setting GITHUB_TOKEN: %v", err)
				os.Exit(1)
			}

			err = writeToEnvFile("GITHUB_TOKEN", token)
			if err != nil {
				color.Red("Error writing GITHUB_TOKEN to config file: %v", err)
				os.Exit(1)
			}
			color.Green("GITHUB_TOKEN set successfully")
		}

		if weatherKey != "" {
			err := os.Setenv("WEATHER_API_KEY", weatherKey)
			if err != nil {
				color.Red("Error setting WEATHER_API_KEY: %v", err)
				os.Exit(1)
			}

			err = writeToEnvFile("WEATHER_API_KEY", weatherKey)
			if err != nil {
				color.Red("Error writing WEATHER_API_KEY to config file: %v", err)
				os.Exit(1)
			}
			color.Green("WEATHER_API_KEY set successfully")
		}

		color.Cyan("Configuration set successfully")
	},
}

func init() {
	configCmd.Flags().StringVarP(&token, "token", "t", "", "GitHub token to set")
	configCmd.Flags().StringVarP(&weatherKey, "weather", "w", "", "Weather API key to set")
	rootCmd.AddCommand(configCmd)
}

func writeToEnvFile(key, value string) error {
	configFile, err := os.OpenFile(".env", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return fmt.Errorf("error opening config file: %w", err)
	}
	defer configFile.Close()

	_, err = configFile.WriteString(fmt.Sprintf("%s=%s\n", key, value))
	if err != nil {
		return fmt.Errorf("error writing to config file: %w", err)
	}

	return nil
}
