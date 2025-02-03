package handlers

import (
	mocks "forum/internal/repo/mocks"
	"net/http"
	"net/url"
	"os"
	"testing"

	"github.com/sirupsen/logrus"
)

var Log = logrus.New()

func InitLogger() {
	Log.SetOutput(os.Stdout)
	Log.SetFormatter(&logrus.TextFormatter{
		FullTimestamp: true,
	})
	Log.SetLevel(logrus.InfoLevel)
}

func TestMain(m *testing.M) {
	InitLogger()
	logrus.Info("=== Starting Test Suite ===")

	exitCode := m.Run()

	logrus.Info("=== Test Suite Completed ===")

	os.Exit(exitCode)
}
func TestSignUp(t *testing.T) {
	// You already have a test server
	ts := NewTestServer(t)
	defer ts.Close()

	logrus.Info("TestSignUp: Starting table-driven tests for /signup")

	const (
		validUsername = "max"
		validEmail    = "max@gmail.com"
		validPassword = "max@gmail.com"
	)

	tests := []struct {
		name          string
		username      string
		email         string
		password      string
		passwordAgain string
		wantCode      int
	}{
		{
			name:          "Valid signup",
			username:      validUsername,
			email:         validEmail,
			password:      validPassword,
			passwordAgain: validPassword,
			wantCode:      http.StatusSeeOther,
		},
		{
			name:          "Blank username",
			username:      "",
			email:         validEmail,
			password:      validPassword,
			passwordAgain: validPassword,
			wantCode:      http.StatusUnprocessableEntity,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			logrus.Infof("Running test case: %q", tt.name)

			form := url.Values{}
			form.Add("name", tt.username)
			form.Add("email", tt.email)
			form.Add("password", tt.password)
			form.Add("password", tt.passwordAgain)

			code, _, _ := ts.postForm(t, "/signup", form)

			// Compare code to expected
			if code != tt.wantCode {
				logrus.Errorf(
					"Signup test FAILED for %q: got code %d, want %d",
					tt.name, code, tt.wantCode,
				)
			} else {
				logrus.Infof(
					"Signup test PASSED for %q: got code %d (as expected)",
					tt.name, code,
				)
			}

			// Original assertion
			mocks.Equal(t, code, tt.wantCode)
		})
	}

	logrus.Info("TestSignUp: Completed table-driven tests for /signup")
}

func TestUserLoginPost(t *testing.T) {
	ts := NewTestServer(t)
	defer ts.Close()

	logrus.Info("TestUserLoginPost: Starting table-driven tests for /login")

	const (
		validEmail    = "max@gmail.com"
		validPassword = "maxmax01"
	)

	tests := []struct {
		name     string
		email    string
		password string
		wantCode int
	}{

		{
			name:     "Incorrect email",
			email:    "naaaaaaaah@gmail.com@gmail.com",
			password: validPassword,
			wantCode: http.StatusUnprocessableEntity,
		},
		{
			name:     "Valid login",
			email:    validEmail,
			password: validPassword,
			wantCode: http.StatusSeeOther,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			logrus.Infof("Running test case: %q", tt.name)

			form := url.Values{}
			form.Add("email", tt.email)
			form.Add("password", tt.password)
			code, _, _ := ts.postForm(t, "/login", form)

			if code != tt.wantCode {
				logrus.Errorf(
					"Login test FAILED for %q: got %d, want %d",
					tt.name, code, tt.wantCode,
				)
			} else {
				logrus.Infof(
					"Login test PASSED for %q: got %d (as expected)",
					tt.name, code,
				)
			}

			mocks.Equal(t, code, tt.wantCode)
		})
	}

	logrus.Info("TestUserLoginPost: Completed table-driven tests for /login")
}
