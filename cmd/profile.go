package cmd

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"strings"

	"github.com/AlecAivazis/survey/v2"
	"github.com/go-resty/resty/v2"
	"github.com/google/go-github/v50/github"
	"github.com/joho/godotenv"
	"github.com/spf13/cobra"
	"golang.org/x/oauth2"
)

var (
	name        string
	bioChoice   string
	bioFlag     bool
	location    string
	customBio   string
	githubToken string
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

		githubToken = os.Getenv("GITHUB_TOKEN")
		if githubToken == "" {
			fmt.Println("GITHUB_TOKEN is not set")
			os.Exit(1)
		}

		// Vérifier les flags fournis
		if !bioFlag && name == "" {
			cmd.Help()
			return
		}

		if bioFlag {
			// Menu interactif pour choisir l'option de mise à jour de la bio
			options := []string{"Weather info", "Total commits", "Custom bio"}
			prompt := &survey.Select{
				Message: "Choose the information to update your bio:",
				Options: options,
			}
			survey.AskOne(prompt, &bioChoice)

			switch bioChoice {
			case "Weather info":
				if location == "" {
					prompt := &survey.Input{
						Message: "Enter your location:",
					}
					survey.AskOne(prompt, &location)
				}
				bio := getWeather(location)
				updateGitHubProfile(name, bio)
			case "Total commits":
				commits := getTotalCommits(githubToken)
				bio := fmt.Sprintf("Total commits: %d", commits)
				updateGitHubProfile(name, bio)
			case "Custom bio":
				prompt := &survey.Input{
					Message: "Enter your custom bio:",
				}
				survey.AskOne(prompt, &customBio)
				updateGitHubProfile(name, customBio)
			}
		}

		if name != "" {
			updateGitHubProfile(name, "")
		}
	},
}

func init() {
	profileCmd.Flags().StringVarP(&name, "name", "n", "", "Name to set")
	profileCmd.Flags().BoolVarP(&bioFlag, "bio", "b", false, "Bio flag to trigger bio update menu")
	rootCmd.AddCommand(profileCmd)
}

func updateGitHubProfile(name, bio string) {
	ctx := context.Background()
	ts := oauth2.StaticTokenSource(
		&oauth2.Token{AccessToken: githubToken},
	)
	tc := oauth2.NewClient(ctx, ts)

	client := github.NewClient(tc)

	user := &github.User{
		Name: github.String(name),
	}
	if bio != "" {
		user.Bio = github.String(bio)
	}

	_, _, err := client.Users.Edit(ctx, user)
	if err != nil {
		fmt.Printf("Error updating profile: %v\n", err)
		os.Exit(1)
	}

	fmt.Println("Profile updated successfully")
}

func getWeather(location string) string {
	client := resty.New()
	apiKey := os.Getenv("WEATHER_API_KEY")
	if apiKey == "" {
		fmt.Println("WEATHER_API_KEY is not set")
		os.Exit(1)
	}

	resp, err := client.R().
		SetQueryParams(map[string]string{
			"q":     location,
			"appid": apiKey,
			"units": "metric",
		}).
		Get("https://api.openweathermap.org/data/2.5/weather")

	if err != nil {
		fmt.Printf("Error fetching weather: %v\n", err)
		os.Exit(1)
	}

	var result map[string]interface{}
	if err := json.Unmarshal(resp.Body(), &result); err != nil {
		fmt.Printf("Error parsing weather data: %v\n", err)
		os.Exit(1)
	}

	weather := result["weather"].([]interface{})[0].(map[string]interface{})["description"].(string)
	temp := result["main"].(map[string]interface{})["temp"].(float64)

	return fmt.Sprintf("Weather in %s: %s, %.1f°C", location, strings.Title(weather), temp)
}

func getTotalCommits(token string) int {
	ctx := context.Background()
	ts := oauth2.StaticTokenSource(
		&oauth2.Token{AccessToken: token},
	)
	tc := oauth2.NewClient(ctx, ts)

	client := github.NewClient(tc)

	repos, _, err := client.Repositories.List(ctx, "", nil)
	if err != nil {
		fmt.Printf("Error fetching repositories: %v\n", err)
		os.Exit(1)
	}

	totalCommits := 0
	for _, repo := range repos {
		commits, _, err := client.Repositories.ListCommits(ctx, *repo.Owner.Login, *repo.Name, nil)
		if err != nil {
			fmt.Printf("Error fetching commits for repository %s: %v\n", *repo.Name, err)
			continue
		}
		totalCommits += len(commits)
	}

	return totalCommits
}
