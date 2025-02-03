package handlers

import (
	"fmt"
	"net/http"
	"net/url"
	"os"
	"strconv"
	"testing"
	"time"

	"github.com/sirupsen/logrus"
	"github.com/xuri/excelize/v2"

	"github.com/tebeka/selenium"

	mocks "forum/internal/repo/mocks"
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

// ----- Helper types and functions to load Excel test data -----

type SignupTestCase struct {
	Name          string
	Username      string
	Email         string
	Password      string
	PasswordAgain string
	WantCode      int
}

func loadSignupTestData(fileName, sheetName string) ([]SignupTestCase, error) {
	f, err := excelize.OpenFile(fileName)
	if err != nil {
		return nil, fmt.Errorf("failed to open file %s: %v", fileName, err)
	}
	rows, err := f.GetRows(sheetName)
	if err != nil {
		return nil, fmt.Errorf("failed to get rows from sheet %s: %v", sheetName, err)
	}

	var tests []SignupTestCase
	// Assume first row is header; then each row is: Name | Username | Email | Password | PasswordAgain | WantCode
	for i, row := range rows {
		if i == 0 {
			continue // skip header row
		}
		if len(row) < 6 {
			// not enough columns, skip this row
			continue
		}
		wantCode, err := strconv.Atoi(row[5])
		if err != nil {
			return nil, fmt.Errorf("invalid WantCode in row %d: %w", i, err)
		}
		testCase := SignupTestCase{
			Name:          row[0],
			Username:      row[1],
			Email:         row[2],
			Password:      row[3],
			PasswordAgain: row[4],
			WantCode:      wantCode,
		}
		tests = append(tests, testCase)
	}
	return tests, nil
}

// LoginTestCase represents one test case for /login.
type LoginTestCase struct {
	Name     string
	Email    string
	Password string
	WantCode int
}

// loadLoginTestData loads login test cases from an Excel file.
func loadLoginTestData(fileName, sheetName string) ([]LoginTestCase, error) {
	f, err := excelize.OpenFile(fileName)
	if err != nil {
		return nil, fmt.Errorf("failed to open file %s: %v", fileName, err)
	}
	rows, err := f.GetRows(sheetName)
	if err != nil {
		return nil, fmt.Errorf("failed to get rows from sheet %s: %v", sheetName, err)
	}

	var tests []LoginTestCase
	// Assume first row is header; then each row is: Name | Email | Password | WantCode
	for i, row := range rows {
		if i == 0 {
			continue
		}
		if len(row) < 4 {
			continue
		}
		wantCode, err := strconv.Atoi(row[3])
		if err != nil {
			return nil, fmt.Errorf("invalid WantCode in row %d: %v", i, err)
		}
		testCase := LoginTestCase{
			Name:     row[0],
			Email:    row[1],
			Password: row[2],
			WantCode: wantCode,
		}
		tests = append(tests, testCase)
	}
	return tests, nil
}

// ----- Modified Unit Tests Using Excel Data -----

func TestSignUp(t *testing.T) {
	ts := NewTestServer(t)
	defer ts.Close()

	logrus.Info("TestSignUp: Starting Excel-driven tests for /signup")

	signupTests, err := loadSignupTestData("testdata_signup.xlsx", "Sheet1")
	if err != nil {
		t.Fatalf("Error loading signup test data: %v", err)
	}

	for _, tt := range signupTests {
		t.Run(tt.Name, func(t *testing.T) {
			logrus.Infof("Running signup test case: %q", tt.Name)

			form := url.Values{}
			form.Add("name", tt.Username)
			form.Add("email", tt.Email)
			form.Add("password", tt.Password)
			form.Add("password", tt.PasswordAgain)

			code, _, _ := ts.postForm(t, "/signup", form)

			if code != tt.WantCode {
				logrus.Errorf("Signup test FAILED for %q: got code %d, want %d", tt.Name, code, tt.WantCode)
			} else {
				logrus.Infof("Signup test PASSED for %q: got code %d (as expected)", tt.Name, code)
			}
			// Use your custom assertion (or t.Errorf)
			mocks.Equal(t, code, tt.WantCode)
		})
	}
	logrus.Info("TestSignUp: Completed Excel-driven tests for /signup")
}

func TestUserLoginPost(t *testing.T) {
	ts := NewTestServer(t)
	defer ts.Close()

	logrus.Info("TestUserLoginPost: Starting Excel-driven tests for /login")

	loginTests, err := loadLoginTestData("testdata_login.xlsx", "Sheet1")
	if err != nil {
		t.Fatalf("Error loading login test data: %v", err)
	}

	for _, tt := range loginTests {
		t.Run(tt.Name, func(t *testing.T) {
			logrus.Infof("Running login test case: %q", tt.Name)

			form := url.Values{}
			form.Add("email", tt.Email)
			form.Add("password", tt.Password)
			fmt.Println(form)
			code, _, _ := ts.postForm(t, "/login", form)

			if code != tt.WantCode {
				logrus.Errorf("Login test FAILED for %q: got %d, want %d", tt.Name, code, tt.WantCode)
			} else {
				logrus.Infof("Login test PASSED for %q: got %d (as expected)", tt.Name, code)
			}
			mocks.Equal(t, code, tt.WantCode)
		})
	}
	logrus.Info("TestUserLoginPost: Completed Excel-driven tests for /login")
}

// ----- E2E Test via BrowserStack Using Selenium -----
//
// This test demonstrates how you might use BrowserStack to perform a
// real browser-based (Selenium) test on your deployed forum login page.
// The test data for login is again read from Excel.
// You must ensure your Forum is accessible from BrowserStack (e.g. via a public URL
// or by using BrowserStack’s local testing tunnel).
func TestUserLoginBrowserStack(t *testing.T) {
	logrus.Info("TestUserLoginBrowserStack: Starting BrowserStack E2E tests for /login")

	// Load login test data from Excel
	loginTests, err := loadLoginTestData("testdata_login.xlsx", "Sheet1")
	if err != nil {
		t.Fatalf("Error loading login test data: %v", err)
	}

	// Retrieve BrowserStack credentials from environment variables.
	// (Set BROWSERSTACK_USER and BROWSERSTACK_KEY in your environment.)
	bsUser := "cowbuno_7Tam42"
	bsKey := "QJsbG7ySCnDoqzB2tFt9"
	// if bsUser == "" || bsKey == "" {
	// 	t.Fatal("BrowserStack credentials are not set in environment variables")
	// }

	// Define desired capabilities.
	caps := selenium.Capabilities{
		"browserName":     "Chrome",
		"browser_version": "latest",
		"os":              "Windows",
		"os_version":      "10",
	}
	caps["browserstack.user"] = bsUser
	caps["browserstack.key"] = bsKey

	// BrowserStack hub URL
	bsHubURL := "http://hub-cloud.browserstack.com/wd/hub"
	wd, err := selenium.NewRemote(caps, bsHubURL)
	if err != nil {
		t.Fatalf("Failed to create remote WebDriver: %v", err)
	}
	defer wd.Quit()

	// URL of your deployed forum login page.
	// Ensure this is accessible from BrowserStack.
	forumURL := "http://your-forum-app-url.com/login" // <-- REPLACE with your actual URL

	for _, tc := range loginTests {
		t.Run(tc.Name, func(t *testing.T) {
			// Navigate to the login page.
			if err := wd.Get(forumURL); err != nil {
				t.Fatalf("Failed to navigate to login page: %v", err)
			}

			// Wait for the page to load.
			time.Sleep(3 * time.Second)

			// Fill in login form fields.
			// Adjust selectors (ByID, ByCSSSelector, etc.) as needed.
			emailElem, err := wd.FindElement(selenium.ByID, "email-login")
			if err != nil {
				t.Fatalf("Failed to find email input: %v", err)
			}
			passwordElem, err := wd.FindElement(selenium.ByID, "password-login")
			if err != nil {
				t.Fatalf("Failed to find password input: %v", err)
			}
			emailElem.Clear()
			emailElem.SendKeys(tc.Email)
			passwordElem.Clear()
			passwordElem.SendKeys(tc.Password)

			// Click the login button.
			loginButton, err := wd.FindElement(selenium.ByID, "login-button")
			if err != nil {
				t.Fatalf("Failed to find login button: %v", err)
			}
			if err := loginButton.Click(); err != nil {
				t.Fatalf("Failed to click login button: %v", err)
			}

			// Allow time for the login action to process.
			time.Sleep(5 * time.Second)

			// Validate the outcome based on your expectation.
			// For example, suppose a successful login shows an element with ID "user-home"
			// and a failed login shows an element with ID "login-error".
			if tc.WantCode == http.StatusOK {
				// Check for an element that appears only on a successful login.
				if _, err := wd.FindElement(selenium.ByID, "user-home"); err != nil {
					t.Errorf("Expected successful login, but did not find element 'user-home': %v", err)
				}
			} else {
				// Check for a login error indicator.
				if _, err := wd.FindElement(selenium.ByID, "login-error"); err != nil {
					t.Errorf("Expected login error, but did not find element 'login-error': %v", err)
				}
			}
		})
	}

	logrus.Info("TestUserLoginBrowserStack: Completed BrowserStack E2E tests for /login")
}
