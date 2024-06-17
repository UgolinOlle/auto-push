package main

import (
	"fmt"

	"github.com/mbndr/figlet4go"
	"github.com/ugolinolle/auto-push/cmd"
)

func main() {
	ascii := figlet4go.NewAsciiRender()
	options := figlet4go.NewRenderOptions()
	options.FontColor = []figlet4go.Color{
		figlet4go.ColorGreen,
		figlet4go.ColorYellow,
		figlet4go.ColorRed,
	}

	renderStr, _ := ascii.RenderOpts("Auto-Push", options)
	fmt.Print(renderStr)
	fmt.Println()

	cmd.Execute()
}
