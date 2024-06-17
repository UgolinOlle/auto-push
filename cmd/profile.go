package cmd

import (
	"context"
	"fmt"
	"github.com/google/go-github/v50/github"
	"golang.org/x/oauth2"
	"os"

	"github.com/joho/godotenv"
	"github.com/spf13/cobra"
)

var (
	name string
	bio  string
)

var profileCmd = &cobra.Command{
	Use:   "profile",
	Short: "Update GitHub profile",
	Run: func(cmd *cobra.Command, args []string) {
		err := godotenv.Load()
		if err != nil {
			fmt.Println("Error loading .env file")
			os.Exit(1)
		}

		token := os.Getenv("GITHUB_TOKEN")
		if token == "" {
			fmt.Println("GITHUB_TOKEN is not set")
			os.Exit(1)
		}

		ctx := context.Background()
		ts := oauth2.StaticTokenSource(
			&oauth2.Token{AccessToken: token},
		)
		tc := oauth2.NewClient(ctx, ts)

		client := github.NewClient(tc)

		user := &github.User{
			Name: github.String(name),
			Bio:  github.String(bio),
		}

		_, _, err = client.Users.Edit(ctx, user)
		if err != nil {
			fmt.Printf("Error updating profile: %v\n", err)
			os.Exit(1)
		}

		fmt.Println("Profile updated successfully")
	},
}

func init() {
	profileCmd.Flags().StringVarP(&name, "name", "n", "", "Name to set")
	profileCmd.Flags().StringVarP(&bio, "bio", "b", "", "Bio to set")
	rootCmd.AddCommand(profileCmd)
}
