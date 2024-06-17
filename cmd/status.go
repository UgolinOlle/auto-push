package cmd

import (
	"context"
	"net/http"
	"os"
	"time"

	"github.com/AlecAivazis/survey/v2"
	"github.com/briandowns/spinner"
	"github.com/enescakir/emoji"
	"github.com/fatih/color"
	"github.com/joho/godotenv"
	"github.com/machinebox/graphql"
	"github.com/spf13/cobra"
)

var (
	message    string
	emojiInput string
)

var statusCmd = &cobra.Command{
	Use:   "status",
	Short: "Update GitHub profile status",
	Run: func(cmd *cobra.Command, args []string) {
		err := godotenv.Load()
		if err != nil {
			color.Red("Error loading .env file")
			os.Exit(1)
		}

		token := os.Getenv("GITHUB_TOKEN")
		if token == "" {
			color.Red("GITHUB_TOKEN is not set")
			os.Exit(1)
		}

		// Prompt for message if not provided
		if message == "" {
			prompt := &survey.Input{
				Message: "Enter your status message:",
			}
			survey.AskOne(prompt, &message)
		}

		// Prompt for emoji if not provided
		if emojiInput == "" {
			prompt := &survey.Input{
				Message: "Enter your status emoji:",
			}
			survey.AskOne(prompt, &emojiInput)
		}

		// Prompts for confirmation
		var confirm bool
		prompt := &survey.Confirm{
			Message: "Do you want to update your GitHub status?",
		}
		survey.AskOne(prompt, &confirm)
		if !confirm {
			color.Yellow("Operation cancelled")
			return
		}

		s := spinner.New(spinner.CharSets[9], 100*time.Millisecond) // Build our new spinner
		s.Start()                                                   // Start the spinner
		defer s.Stop()                                              // Stop the spinner when done

		httpClient := &http.Client{}
		client := graphql.NewClient("https://api.github.com/graphql", graphql.WithHTTPClient(httpClient))
		req := graphql.NewRequest(`
            mutation($input: ChangeUserStatusInput!) {
                changeUserStatus(input: $input) {
                    status {
                        message
                        emoji
                    }
                }
            }
        `)

		req.Var("input", map[string]interface{}{
			"message": message,
			"emoji":   emoji.Parse(emojiInput),
		})

		req.Header.Set("Authorization", "Bearer "+token)

		ctx := context.Background()
		var respData interface{}
		err = client.Run(ctx, req, &respData)
		if err != nil {
			color.Red("Error updating status: %v", err)
			os.Exit(1)
		}

		color.Green("Status updated successfully")
	},
}

func init() {
	statusCmd.Flags().StringVarP(&message, "message", "m", "", "Status message to set")
	statusCmd.Flags().StringVarP(&emojiInput, "emoji", "e", "", "Status emoji to set")
	rootCmd.AddCommand(statusCmd)
}
