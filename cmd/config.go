package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
)

var token string

var configCmd = &cobra.Command{
	Use:   "config",
	Short: "Configure GitHub token",
	Run: func(cmd *cobra.Command, args []string) {
		err := os.Setenv("GITHUB_TOKEN", token)
		if err != nil {
			fmt.Printf("Error setting GITHUB_TOKEN: %v\n", err)
			os.Exit(1)
		}

		configFile, err := os.OpenFile(".env", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
		if err != nil {
			fmt.Printf("Error opening config file: %v\n", err)
			os.Exit(1)
		}
		defer configFile.Close()

		_, err = configFile.WriteString(fmt.Sprintf("GITHUB_TOKEN=%s\n", token))
		if err != nil {
			fmt.Printf("Error writing to config file: %v\n", err)
			os.Exit(1)
		}

		fmt.Println("GITHUB_TOKEN set successfully")
	},
}

func init() {
	configCmd.Flags().StringVarP(&token, "token", "t", "", "GitHub token to set")
	configCmd.MarkFlagRequired("token")
	rootCmd.AddCommand(configCmd)
}
