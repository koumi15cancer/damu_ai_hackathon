import React, { useState, useEffect } from "react";
import {
  CircularProgress,
  Rating,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  SelectChangeEvent,
  Menu,
  MenuItem,
} from "@mui/material";
import {
  ExpandMore,
  LocationOn,
  AttachMoney,
  Group,
  EmojiEvents,
  Directions,
  Lightbulb,
  Nature,
  SportsEsports,
  Palette,
} from "@mui/icons-material";
import axios from "axios";
import History from "./History";
import TeamMemberManagement from "./TeamMemberManagement";
import AnalyticsSuggestions from "./AnalyticsSuggestions";
import UIStyleDemo from "./components/UIStyleDemo";
import { Button } from "./components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./components/ui/card";
import { Input } from "./components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./components/ui/select";
import { Checkbox } from "./components/ui/checkbox";
import { Label } from "./components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "./components/ui/dialog";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import { cn } from "./lib/utils";
import { Badge } from "./components/ui/badge";
import {
  Alert,
  AlertDescription,
  AlertTitle,
} from "./components/ui/alert";

interface TeamMember {
  id: string;
  name: string;
  location: string;
  preferences: string[];
  vibe: string;
}

interface EventPhase {
  activity: string;
  location: string;
  map_link: string;
  cost: number;
  indicators: string[];
}

interface EventPlan {
  phases: EventPhase[];
  total_cost: number;
  contribution_needed: number;
  fit_analysis: string;
  rating: number;
}

interface UserPreferences {
  theme: string;
  budget_contribution: string;
  available_members: string[];
  date_time?: string;
  location_zone?: string;
}

function App() {
  const [teamMembers, setTeamMembers] = useState<TeamMember[]>([]);
  const [plans, setPlans] = useState<EventPlan[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");
  const [selectedPlan, setSelectedPlan] = useState<EventPlan | null>(null);
  const [planDialogOpen, setPlanDialogOpen] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState("planner");
  const [saveSuccessDialogOpen, setSaveSuccessDialogOpen] =
    useState<boolean>(false);
  const [savingPlan, setSavingPlan] = useState<boolean>(false);
  const [duplicateDialogOpen, setDuplicateDialogOpen] = useState<boolean>(false);
  const [analyticsSuggestions, setAnalyticsSuggestions] = useState<any>(null);
  const [currentTheme, setCurrentTheme] = useState<string>("dark");
  const [themeMenuAnchor, setThemeMenuAnchor] = useState<null | HTMLElement>(
    null
  );

  const themes = [
    { name: "default", label: "Default", class: "" },
    { name: "light-pink", label: "Light Pink", class: "light-pink" },
    { name: "light-purple", label: "Light Purple", class: "light-purple" },
    { name: "light-yellow", label: "Light Yellow", class: "light-yellow" },
    { name: "light-orange", label: "Light Orange", class: "light-orange" },
    { name: "light-green", label: "Light Green", class: "light-green" },
    { name: "light-blue", label: "Light Blue", class: "light-blue" },
    { name: "dark", label: "Dark", class: "dark" },
    { name: "dark-pink", label: "Dark Pink", class: "dark-pink" },
    { name: "dark-purple", label: "Dark Purple", class: "dark-purple" },
    { name: "dark-yellow", label: "Dark Yellow", class: "dark-yellow" },
    { name: "dark-orange", label: "Dark Orange", class: "dark-orange" },
    { name: "dark-green", label: "Dark Green", class: "dark-green" },
    { name: "dark-blue", label: "Dark Blue", class: "dark-blue" },
  ];

  const changeTheme = (themeClass: string) => {
    themes.forEach((theme) => {
      if (theme.class && theme.class.trim() !== "") {
        document.body.classList.remove(theme.class);
      }
    });

    if (themeClass && themeClass.trim() !== "") {
      document.body.classList.add(themeClass);
    }

    setCurrentTheme(themeClass || "default");
    setThemeMenuAnchor(null);
  };

  const handleThemeMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setThemeMenuAnchor(event.currentTarget);
  };

  const handleThemeMenuClose = () => {
    setThemeMenuAnchor(null);
  };

  const [userPreferences, setUserPreferences] = useState<UserPreferences>({
    theme: "fun 🎉",
    budget_contribution: "No",
    available_members: [],
    date_time: "",
    location_zone: "",
  });

  useEffect(() => {
    loadTeamMembers();
    loadAnalyticsSuggestions();
    changeTheme("dark");
  }, []);

  const loadTeamMembers = async () => {
    try {
      const response = await axios.get("http://localhost:5000/team-members");
      setTeamMembers(response.data);
      setUserPreferences((prev: UserPreferences) => ({
        ...prev,
        available_members: response.data.map(
          (member: TeamMember) => member.name
        ),
      }));
    } catch (error) {
      console.error("Failed to load team members:", error);
      setError(
        "Failed to load team members. Please check if the backend server is running."
      );
    }
  };

  const loadAnalyticsSuggestions = async () => {
    try {
      const response = await axios.get(
        "http://localhost:5000/analytics/suggestions?limit=5"
      );
      setAnalyticsSuggestions(response.data);
    } catch (error) {
      console.error("Failed to load suggestions:", error);
    }
  };

  const handleGeneratePlans = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await axios.post(
        "http://localhost:5000/generate-plans",
        userPreferences
      );

      if (response.data.error) {
        setError(response.data.error);
        setPlans([]);
        return;
      }

      setPlans(response.data);
    } catch (error) {
      console.error("Failed to generate plans:", error);
      setError("Failed to generate team bonding plans. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleMemberToggle = (memberName: string) => {
    setUserPreferences((prev: UserPreferences) => {
      const isMemberSelected = prev.available_members.includes(memberName);
      return {
        ...prev,
        available_members: isMemberSelected
          ? prev.available_members.filter((name) => name !== memberName)
          : [...prev.available_members, memberName],
      };
    });
  };

  const handlePlanClick = (plan: EventPlan) => {
    setSelectedPlan(plan);
    setPlanDialogOpen(true);
  };

  const handleSavePlan = async () => {
    if (!selectedPlan) return;

    try {
      setSavingPlan(true);

      const planData = {
        date:
          userPreferences.date_time || new Date().toISOString().split("T")[0],
        theme: userPreferences.theme,
        location: userPreferences.location_zone || "Ho Chi Minh City",
        participants: userPreferences.available_members,
        activities: selectedPlan.phases.map((phase) => phase.activity),
        total_cost: selectedPlan.total_cost,
        phases: selectedPlan.phases,
        fit_analysis: selectedPlan.fit_analysis,
        rating: selectedPlan.rating,
        contribution_needed: selectedPlan.contribution_needed,
      };

      await axios.post("http://localhost:5000/event-history", planData);

      setPlanDialogOpen(false);
      setSelectedPlan(null);
      setSaveSuccessDialogOpen(true);
    } catch (error: any) {
      console.error("Failed to save plan:", error);

      if (error.response && error.response.status === 409) {
        setDuplicateDialogOpen(true);
      } else {
        alert("Failed to save plan. Please try again.");
      }
    } finally {
      setSavingPlan(false);
    }
  };

  const getThemeIcon = (theme: string) => {
    switch (theme) {
      case "fun 🎉":
        return <EmojiEvents />;
      case "chill 🧘":
        return <Nature />;
      case "outdoor 🌤":
        return <SportsEsports />;
      default:
        return <Group />;
    }
  };

  const renderEventPlanner = () => (
    <div className="space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-foreground">
          Team Bonding Event Planner
        </h1>
        <p className="text-muted-foreground">
          Generate personalized team bonding plans based on member preferences
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Event Preferences</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label>Event Theme</Label>
              <Select
                value={userPreferences.theme}
                onValueChange={(value) =>
                  setUserPreferences((prev) => ({ ...prev, theme: value }))
                }
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select a theme" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="fun 🎉">Fun 🎉</SelectItem>
                  <SelectItem value="chill 🧘">Chill 🧘</SelectItem>
                  <SelectItem value="outdoor 🌤">Outdoor 🌤</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Budget Contribution</Label>
              <Select
                value={userPreferences.budget_contribution}
                onValueChange={(value) =>
                  setUserPreferences((prev) => ({
                    ...prev,
                    budget_contribution: value,
                  }))
                }
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select budget" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="No">No additional contribution</SelectItem>
                  <SelectItem value="Yes, up to 50,000 VND">
                    Yes, up to 50,000 VND
                  </SelectItem>
                  <SelectItem value="Yes, up to 100,000 VND">
                    Yes, up to 100,000 VND
                  </SelectItem>
                  <SelectItem value="Yes, up to 150,000 VND">
                    Yes, up to 150,000 VND
                  </SelectItem>
                  <SelectItem value="Yes, up to 200,000 VND">
                    Yes, up to 200,000 VND
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Preferred Date & Time</Label>
              <Input
                type="datetime-local"
                value={userPreferences.date_time}
                onChange={(e) =>
                  setUserPreferences((prev) => ({
                    ...prev,
                    date_time: e.target.value,
                  }))
                }
              />
            </div>
            <div>
              <Label>Preferred Location Zone</Label>
              <Input
                placeholder="e.g., District 1"
                value={userPreferences.location_zone}
                onChange={(e) =>
                  setUserPreferences((prev) => ({
                    ...prev,
                    location_zone: e.target.value,
                  }))
                }
              />
            </div>
          </div>

          <div>
            <h3 className="text-lg font-medium text-foreground mb-2">
              Available Team Members
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {teamMembers.map((member) => (
                <div key={member.id} className="flex items-center space-x-2">
                  <Checkbox
                    id={member.id}
                    checked={userPreferences.available_members.includes(
                      member.name
                    )}
                    onCheckedChange={() => handleMemberToggle(member.name)}
                  />
                  <Label
                    htmlFor={member.id}
                    className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  >
                    <span className="block">{member.name}</span>
                    <span className="text-xs text-muted-foreground">
                      {member.vibe} • {member.location}
                    </span>
                  </Label>
                </div>
              ))}
            </div>
          </div>

          <div>
            <Button
              onClick={handleGeneratePlans}
              disabled={
                loading || userPreferences.available_members.length === 0
              }
              size="lg"
            >
              {loading && (
                <CircularProgress
                  size={20}
                  color="inherit"
                  className="mr-2"
                />
              )}
              {loading ? "Generating Plans..." : "Generate Event Plans"}
            </Button>
          </div>

          {analyticsSuggestions &&
            analyticsSuggestions.suggestions &&
            analyticsSuggestions.suggestions.length > 0 && (
              <Card className="bg-muted/50">
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Lightbulb className="mr-2 text-yellow-500" />
                    AI Suggestions for Better Events
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground mb-4">
                    Based on your recent events, here are some insights to
                    improve your team bonding:
                  </p>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {analyticsSuggestions.suggestions
                      .slice(0, 2)
                      .map((suggestion: any, index: number) => (
                        <Card key={index} className="bg-background">
                          <CardHeader>
                            <CardTitle className="text-base text-primary">
                              {suggestion.title}
                            </CardTitle>
                          </CardHeader>
                          <CardContent>
                            <p className="text-sm text-muted-foreground">
                              {suggestion.description}
                            </p>
                            <p className="text-xs text-muted-foreground mt-2">
                              Confidence:{" "}
                              {Math.round(suggestion.confidence * 100)}%
                            </p>
                          </CardContent>
                        </Card>
                      ))}
                  </div>
                </CardContent>
              </Card>
            )}
        </CardContent>
      </Card>

      {error && (
        <Alert variant="destructive">
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {plans.length > 0 && (
        <div>
          <h2 className="text-2xl font-bold text-foreground mb-4">
            Generated Plans ({plans.length})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {plans.map((plan, index) => (
              <Card
                key={index}
                className="cursor-pointer transition-transform hover:-translate-y-1"
                onClick={() => handlePlanClick(plan)}
              >
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <div className="p-2 mr-3 bg-primary/10 rounded-full text-primary">
                      {getThemeIcon(userPreferences.theme)}
                    </div>
                    Plan {index + 1}
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <p className="text-sm text-muted-foreground">
                    {plan.fit_analysis}
                  </p>
                  <div className="flex items-center">
                    <Rating value={plan.rating} readOnly size="small" />
                    <span className="text-sm ml-2">{plan.rating}/5</span>
                  </div>
                  <div className="flex items-center text-muted-foreground">
                    <AttachMoney fontSize="small" className="mr-1" />
                    <span className="text-sm">
                      {plan.total_cost.toLocaleString()} VND
                    </span>
                  </div>
                  {plan.contribution_needed > 0 && (
                    <Alert variant="warning" className="mt-2">
                      <AlertDescription>
                        Additional contribution:{" "}
                        {plan.contribution_needed.toLocaleString()} VND
                      </AlertDescription>
                    </Alert>
                  )}
                  <p className="text-sm text-muted-foreground">
                    {plan.phases.length} phase
                    {plan.phases.length !== 1 ? "s" : ""}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}
    </div>
  );

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <div className="absolute top-4 left-4 z-50">
        <Button
          variant="outline"
          size="icon"
          onClick={handleThemeMenuOpen}
          aria-label="Change theme"
        >
          <Palette />
        </Button>
        <Menu
          anchorEl={themeMenuAnchor}
          open={Boolean(themeMenuAnchor)}
          onClose={handleThemeMenuClose}
        >
          {themes.map((theme) => (
            <MenuItem
              key={theme.name}
              onClick={() => changeTheme(theme.class)}
              selected={currentTheme === theme.name}
            >
              {theme.label}
            </MenuItem>
          ))}
        </Menu>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList>
          <TabsTrigger value="planner">🎉 Event Planner</TabsTrigger>
          <TabsTrigger value="members">👥 Team Members</TabsTrigger>
          <TabsTrigger value="history">📅 History</TabsTrigger>
          <TabsTrigger value="analytics">📊 Analytics</TabsTrigger>
          <TabsTrigger value="demo">🎨 UIStyleDemo</TabsTrigger>
        </TabsList>
        <TabsContent value="planner" className="mt-4">
          {renderEventPlanner()}
        </TabsContent>
        <TabsContent value="members" className="mt-4">
          <TeamMemberManagement />
        </TabsContent>
        <TabsContent value="history" className="mt-4">
          <History />
        </TabsContent>
        <TabsContent value="analytics" className="mt-4">
          <AnalyticsSuggestions />
        </TabsContent>
        <TabsContent value="demo" className="mt-4">
          <UIStyleDemo />
        </TabsContent>
      </Tabs>

      <Dialog open={planDialogOpen} onOpenChange={setPlanDialogOpen}>
        <DialogContent className="max-w-3xl">
          {selectedPlan && (
            <>
              <DialogHeader>
                <DialogTitle className="flex items-center">
                  <div className="p-2 mr-3 bg-primary/10 rounded-full text-primary">
                    {getThemeIcon(userPreferences.theme)}
                  </div>
                  <span className="text-2xl font-bold">
                    Team Bonding Plan
                  </span>
                </DialogTitle>
              </DialogHeader>

              <div className="grid md:grid-cols-3 gap-6 py-4">
                <div className="md:col-span-2 space-y-3">
                  <h3 className="text-lg font-semibold">📍 Event Phases</h3>
                  {selectedPlan.phases.map(
                    (phase: EventPhase, index: number) => (
                      <Accordion key={index} sx={{ mb: 2 }}>
                        <AccordionSummary expandIcon={<ExpandMore />}>
                          <div className="flex justify-between items-center w-full">
                            <h4 className="font-semibold">
                              Phase {index + 1}: {phase.activity}
                            </h4>
                            <Badge>
                              {phase.cost.toLocaleString()} VND
                            </Badge>
                          </div>
                        </AccordionSummary>
                        <AccordionDetails>
                          <List dense>
                            <ListItem>
                              <ListItemIcon>
                                <LocationOn color="primary" />
                              </ListItemIcon>
                              <ListItemText
                                primary="Address"
                                secondary={phase.location}
                              />
                            </ListItem>
                            {phase.map_link && (
                              <ListItem>
                                <ListItemIcon>
                                  <Directions color="primary" />
                                </ListItemIcon>
                                <ListItemText
                                  primary="Google Maps"
                                  secondary={
                                    <a
                                      href={phase.map_link}
                                      target="_blank"
                                      rel="noopener noreferrer"
                                      className="text-blue-500 hover:underline"
                                    >
                                      Open in Maps
                                    </a>
                                  }
                                />
                              </ListItem>
                            )}
                          </List>
                          <div className="flex gap-2 flex-wrap">
                            {phase.indicators.map((indicator, idx) => (
                              <Badge key={idx} variant="secondary">
                                {indicator}
                              </Badge>
                            ))}
                          </div>
                        </AccordionDetails>
                      </Accordion>
                    )
                  )}
                </div>

                <div className="space-y-4">
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">💰 Cost Breakdown</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-3xl font-bold text-green-600">
                        {selectedPlan.total_cost.toLocaleString()} VND
                      </p>
                      <p className="text-sm text-muted-foreground">
                        per person
                      </p>
                      {selectedPlan.contribution_needed > 0 && (
                        <Alert variant="warning" className="mt-2">
                          <AlertDescription>
                            Additional contribution:{" "}
                            {selectedPlan.contribution_needed.toLocaleString()}{" "}
                            VND
                          </AlertDescription>
                        </Alert>
                      )}
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">👥 Team Fit</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-sm text-muted-foreground">
                        {selectedPlan.fit_analysis}
                      </p>
                      <div className="flex items-center mt-2">
                        <Rating
                          value={selectedPlan.rating}
                          readOnly
                          size="small"
                        />
                        <span className="ml-2 text-sm">
                          {selectedPlan.rating}/5
                        </span>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </div>
              <DialogFooter>
                <Button
                  variant="outline"
                  onClick={() => setPlanDialogOpen(false)}
                >
                  Close
                </Button>
                <Button onClick={handleSavePlan} disabled={savingPlan}>
                  {savingPlan && (
                    <CircularProgress
                      size={20}
                      color="inherit"
                      className="mr-2"
                    />
                  )}
                  {savingPlan ? "Saving..." : "Save Plan"}
                </Button>
              </DialogFooter>
            </>
          )}
        </DialogContent>
      </Dialog>

      <Dialog
        open={saveSuccessDialogOpen}
        onOpenChange={setSaveSuccessDialogOpen}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="flex items-center">
              <div className="w-10 h-10 flex items-center justify-center rounded-full bg-green-500 text-white mr-3">
                <span className="text-xl">✓</span>
              </div>
              <span className="font-bold">Plan Saved Successfully!</span>
            </DialogTitle>
          </DialogHeader>
          <DialogDescription className="py-4 space-y-2">
            <p>Your team bonding plan has been saved to the event history.</p>
            <Alert variant="info">
              <AlertDescription>
                You can now view, edit, or delete this plan from the{" "}
                <strong>History tab</strong>.
              </AlertDescription>
            </Alert>
            <p className="text-xs text-muted-foreground">
              The plan includes all phases, costs, and team fit analysis for
              future reference.
            </p>
          </DialogDescription>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => setSaveSuccessDialogOpen(false)}
            >
              Close
            </Button>
            <Button
              onClick={() => {
                setSaveSuccessDialogOpen(false);
                setActiveTab("history");
              }}
            >
              View in History
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Dialog
        open={duplicateDialogOpen}
        onOpenChange={setDuplicateDialogOpen}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="flex items-center">
              <div className="w-10 h-10 flex items-center justify-center rounded-full bg-amber-500 text-white mr-3">
                <span className="text-xl">⚠</span>
              </div>
              <span className="font-bold">Plan Already Exists</span>
            </DialogTitle>
          </DialogHeader>
          <DialogDescription className="py-4 space-y-2">
            <p>A similar plan has already been saved to the event history.</p>
            <Alert variant="warning">
              <AlertDescription>
                This prevents duplicate entries in your history. You can view
                the existing plan in the <strong>History tab</strong>.
              </AlertDescription>
            </Alert>
            <p className="text-xs text-muted-foreground">
              If you want to save a different version, try modifying the plan
              details first.
            </p>
          </DialogDescription>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => setDuplicateDialogOpen(false)}
            >
              Close
            </Button>
            <Button
              onClick={() => {
                setDuplicateDialogOpen(false);
                setActiveTab("history");
              }}
            >
              View in History
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}

export default App;
