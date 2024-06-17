package github

import (
    "context"
    "github.com/google/go-github/v50/github"
)

func UpdateProfile(client *github.Client, name string, bio string) error {
    user := &github.User{
        Name: github.String(name),
        Bio:  github.String(bio),
    }

    _, _, err := client.Users.Edit(context.Background(), user)
    return err
}
