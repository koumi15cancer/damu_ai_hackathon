import React, { useState, useEffect } from "react";
import {
  Box,
  Button,
  TextField,
  Typography,
  Container,
  Paper,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Checkbox,
  FormControlLabel,
  FormGroup,
  Grid,
  Divider,
  Rating,
  Alert,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  SelectChangeEvent,
  Tabs,
  Tab,
  IconButton,
  Avatar,
  AvatarGroup,
  Radio,
  RadioGroup,
} from "@mui/material";
import {
  ExpandMore,
  LocationOn,
  AttachMoney,
  Group,
  Star,
  Restaurant,
  LocalBar,
  SportsEsports,
  Nature,
  EmojiEvents,
  Schedule,
  Directions,
  Psychology,
  Science,
  Settings,
  TrendingUp,
  Lightbulb,
  Analytics,
} from "@mui/icons-material";
import axios from "axios";
import History from "./History";
import TeamMemberManagement from "./TeamMemberManagement";
import AnalyticsSuggestions from "./AnalyticsSuggestions";

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
  ai_model?: string;
  plan_generation_mode?: string;
}

function App() {
  const [teamMembers, setTeamMembers] = useState<TeamMember[]>([]);
  const [plans, setPlans] = useState<EventPlan[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");
  const [selectedPlan, setSelectedPlan] = useState<EventPlan | null>(null);
  const [planDialogOpen, setPlanDialogOpen] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<number>(0);
  const [saveSuccessDialogOpen, setSaveSuccessDialogOpen] =
    useState<boolean>(false);
  const [savingPlan, setSavingPlan] = useState<boolean>(false);
  const [duplicateDialogOpen, setDuplicateDialogOpen] =
    useState<boolean>(false);
  const [analyticsSuggestions, setAnalyticsSuggestions] = useState<any>(null);
  const [loadingSuggestions, setLoadingSuggestions] = useState(false);
  const [availableAIModels, setAvailableAIModels] = useState<string[]>([]);
  const [eventHistory, setEventHistory] = useState<any[]>([]);
  const [historySummary, setHistorySummary] = useState<string>("");

  const [userPreferences, setUserPreferences] = useState<UserPreferences>({
    theme: "fun 🎉",
    budget_contribution: "No",
    available_members: [],
    date_time: "",
    location_zone: "",
    ai_model: "",
    plan_generation_mode: "new",
  });

  // Load team members on component mount
  useEffect(() => {
    loadTeamMembers();
    loadAnalyticsSuggestions();
    loadAvailableAIModels();
    loadEventHistory();
  }, []);

  const loadTeamMembers = async () => {
    try {
      const response = await axios.get("http://localhost:5000/team-members");
      setTeamMembers(response.data);
      // Set all members as available by default
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
    setLoadingSuggestions(true);
    try {
      const response = await axios.get(
        "http://localhost:5000/analytics/suggestions?limit=5"
      );
      setAnalyticsSuggestions(response.data);
    } catch (error) {
      console.error("Failed to load suggestions:", error);
    } finally {
      setLoadingSuggestions(false);
    }
  };

  const loadAvailableAIModels = async () => {
    try {
      const response = await axios.get("http://localhost:5000/ai-models");
      setAvailableAIModels(
        response.data.models || [
          "OpenAI GPT-4",
          "Google Gemini",
          "Anthropic Claude",
        ]
      );
      // Set default AI model if available
      if (
        response.data.models &&
        response.data.models.length > 0 &&
        !userPreferences.ai_model
      ) {
        setUserPreferences((prev: UserPreferences) => ({
          ...prev,
          ai_model: response.data.models[0],
        }));
      }
    } catch (error) {
      console.error("Failed to load AI models:", error);
      // Set fallback models
      setAvailableAIModels([
        "OpenAI GPT-4",
        "Google Gemini",
        "Anthropic Claude",
      ]);
    }
  };

  const loadEventHistory = async () => {
    try {
      const response = await axios.get("http://localhost:5000/event-history");
      setEventHistory(response.data);
      generateHistorySummary(response.data);
    } catch (error) {
      console.error("Failed to load event history:", error);
    }
  };

  const generateHistorySummary = (history: any[]) => {
    if (history.length === 0) {
      setHistorySummary(
        "No previous events found. This will be your first team bonding event!"
      );
      return;
    }

    const recentEvents = history.slice(-3); // Last 3 events
    const themes = Array.from(
      new Set(recentEvents.map((event) => event.theme))
    );
    const locations = Array.from(
      new Set(recentEvents.map((event) => event.location))
    );
    const avgCost = Math.round(
      recentEvents.reduce((sum, event) => sum + event.total_cost, 0) /
        recentEvents.length
    );

    const summary = `Based on your recent ${
      recentEvents.length
    } events, you've enjoyed ${themes.join(", ")} themes in ${locations.join(
      ", "
    )} areas. Average cost per event: ${avgCost.toLocaleString()} VND.`;
    setHistorySummary(summary);
  };

  const handleGeneratePlans = async () => {
    setLoading(true);
    setError("");

    try {
      const requestData = {
        ...userPreferences,
        ai_model: userPreferences.ai_model,
        plan_generation_mode: userPreferences.plan_generation_mode,
      };

      const response = await axios.post(
        "http://localhost:5000/generate-plans",
        requestData
      );

      if (response.data.error) {
        setError(response.data.error);
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
    setUserPreferences((prev: UserPreferences) => ({
      ...prev,
      available_members: prev.available_members.includes(memberName)
        ? prev.available_members.filter((name: string) => name !== memberName)
        : [...prev.available_members, memberName],
    }));
  };

  const handlePlanClick = (plan: EventPlan) => {
    setSelectedPlan(plan);
    setPlanDialogOpen(true);
  };

  const handleSavePlan = async () => {
    if (!selectedPlan) return;

    console.log("💾 Starting plan save process:", {
      planTitle: selectedPlan.phases?.[0]?.activity || "Unknown",
      totalCost: selectedPlan.total_cost,
      participants: userPreferences.available_members.length,
    });

    try {
      setSavingPlan(true);

      // Prepare the plan data for saving
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

      console.log("📤 Saving plan to backend:", {
        date: planData.date,
        theme: planData.theme,
        location: planData.location,
        activitiesCount: planData.activities.length,
      });

      // Save the plan to the backend
      const response = await axios.post(
        "http://localhost:5000/event-history",
        planData
      );

      console.log("✅ Plan saved successfully:", {
        status: response.status,
        planId: response.data?.id || "unknown",
      });

      // Update event history timestamp for analytics triggers
      const updateTimestamp = new Date().toISOString();
      localStorage.setItem("lastEventUpdate", updateTimestamp);

      console.log(
        "🔄 Event history timestamp updated for analytics triggers:",
        {
          timestamp: updateTimestamp,
        }
      );

      // Close the dialog and show success message
      setPlanDialogOpen(false);
      setSelectedPlan(null);
      setSaveSuccessDialogOpen(true);
    } catch (error: any) {
      console.error("❌ Plan save failed:", {
        error: error.message,
        status: error.response?.status,
        data: error.response?.data,
      });

      // Handle duplicate detection from backend
      if (error.response && error.response.status === 409) {
        console.log("⚠️ Duplicate plan detected");
        setDuplicateDialogOpen(true);
      } else {
        alert("Failed to save plan. Please try again.");
      }
    } finally {
      setSavingPlan(false);
      console.log("🏁 Plan save process completed");
    }
  };

  const handleTabChange = (newValue: number) => {
    const tabNames = ["Event Planner", "Team Members", "History", "Analytics"];
    const previousTab = tabNames[activeTab];
    const newTab = tabNames[newValue];

    console.log("🔄 Tab change detected:", {
      from: previousTab,
      to: newTab,
      tabIndex: newValue,
    });

    setActiveTab(newValue);

    // Trigger analytics refresh when switching to Analytics tab
    if (newValue === 3) {
      // Analytics tab
      console.log("📊 Switching to Analytics tab, triggering refresh");
      // Use a small delay to ensure the component is mounted
      setTimeout(() => {
        const analyticsComponent = document.querySelector(
          "[data-analytics-trigger]"
        );
        if (analyticsComponent) {
          console.log(
            "🎯 Analytics component found, dispatching refresh event"
          );
          // Dispatch a custom event to trigger analytics refresh
          window.dispatchEvent(new CustomEvent("refreshAnalytics"));
        } else {
          console.warn("⚠️ Analytics component not found");
        }
      }, 100);
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

  const getThemeColor = (theme: string) => {
    switch (theme) {
      case "fun 🎉":
        return "#ff6b6b";
      case "chill 🧘":
        return "#4ecdc4";
      case "outdoor 🌤":
        return "#45b7d1";
      default:
        return "#95a5a6";
    }
  };

  const renderEventPlanner = () => (
    <Container maxWidth='lg' sx={{ py: 4 }}>
      <Typography variant='h3' component='h1' gutterBottom align='center'>
        Team Bonding Event Planner
      </Typography>
      <Typography
        variant='h6'
        color='text.secondary'
        align='center'
        gutterBottom>
        Generate personalized team bonding plans based on member preferences
      </Typography>

      <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
        <Typography variant='h5' gutterBottom>
          Event Preferences
        </Typography>

        <Grid container spacing={3}>
          {/* Theme Selection */}
          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel>Event Theme</InputLabel>
              <Select
                value={userPreferences.theme}
                label='Event Theme'
                onChange={(e: SelectChangeEvent) =>
                  setUserPreferences((prev: UserPreferences) => ({
                    ...prev,
                    theme: e.target.value,
                  }))
                }>
                <MenuItem value='fun 🎉'>Fun 🎉</MenuItem>
                <MenuItem value='chill 🧘'>Chill 🧘</MenuItem>
                <MenuItem value='outdoor 🌤'>Outdoor 🌤</MenuItem>
              </Select>
            </FormControl>
          </Grid>

          {/* Budget Contribution */}
          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel>Budget Contribution</InputLabel>
              <Select
                value={userPreferences.budget_contribution}
                label='Budget Contribution'
                onChange={(e: SelectChangeEvent) =>
                  setUserPreferences((prev: UserPreferences) => ({
                    ...prev,
                    budget_contribution: e.target.value,
                  }))
                }>
                <MenuItem value='No'>No additional contribution</MenuItem>
                <MenuItem value='Yes, up to 50,000 VND'>
                  Yes, up to 50,000 VND
                </MenuItem>
                <MenuItem value='Yes, up to 100,000 VND'>
                  Yes, up to 100,000 VND
                </MenuItem>
                <MenuItem value='Yes, up to 150,000 VND'>
                  Yes, up to 150,000 VND
                </MenuItem>
                <MenuItem value='Yes, up to 200,000 VND'>
                  Yes, up to 200,000 VND
                </MenuItem>
              </Select>
            </FormControl>
          </Grid>

          {/* Date and Time */}
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label='Preferred Date & Time'
              type='datetime-local'
              value={userPreferences.date_time}
              onChange={(e) =>
                setUserPreferences((prev: UserPreferences) => ({
                  ...prev,
                  date_time: e.target.value,
                }))
              }
              InputLabelProps={{
                shrink: true,
              }}
            />
          </Grid>

          {/* Location Zone */}
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label='Preferred Location Zone'
              placeholder='e.g., District 1'
              value={userPreferences.location_zone}
              onChange={(e) =>
                setUserPreferences((prev: UserPreferences) => ({
                  ...prev,
                  location_zone: e.target.value,
                }))
              }
            />
          </Grid>

          {/* AI Model Selection */}
          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel>AI Model</InputLabel>
              <Select
                value={userPreferences.ai_model}
                label='AI Model'
                onChange={(e: SelectChangeEvent) =>
                  setUserPreferences((prev: UserPreferences) => ({
                    ...prev,
                    ai_model: e.target.value,
                  }))
                }>
                {availableAIModels.map((model) => (
                  <MenuItem key={model} value={model}>
                    {model}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          {/* Event History Summary */}
          {eventHistory.length > 0 && (
            <Grid item xs={12}>
              <Paper
                sx={{
                  p: 3,
                  backgroundColor: "#f8f9fa",
                  border: "1px solid #e9ecef",
                }}>
                <Typography
                  variant='h6'
                  gutterBottom
                  sx={{ display: "flex", alignItems: "center" }}>
                  <Schedule sx={{ mr: 1 }} />
                  Event History Summary
                </Typography>
                <Typography
                  variant='body2'
                  color='text.secondary'
                  sx={{ mb: 2 }}>
                  {historySummary}
                </Typography>

                <Typography variant='subtitle2' gutterBottom>
                  Plan Generation Options:
                </Typography>
                <RadioGroup
                  row
                  value={userPreferences.plan_generation_mode}
                  onChange={(e) =>
                    setUserPreferences((prev: UserPreferences) => ({
                      ...prev,
                      plan_generation_mode: e.target.value,
                    }))
                  }>
                  <FormControlLabel
                    value='reuse'
                    control={<Radio />}
                    label='Reuse previous plan structure'
                  />
                  <FormControlLabel
                    value='similar'
                    control={<Radio />}
                    label='Generate similar plan'
                  />
                  <FormControlLabel
                    value='new'
                    control={<Radio />}
                    label='Create brand new plan'
                  />
                </RadioGroup>
              </Paper>
            </Grid>
          )}

          {/* Team Members */}
          <Grid item xs={12}>
            <Typography variant='h6' gutterBottom>
              Available Team Members
            </Typography>
            <FormGroup row>
              {teamMembers.map((member) => (
                <FormControlLabel
                  key={member.id}
                  control={
                    <Checkbox
                      checked={userPreferences.available_members.includes(
                        member.name
                      )}
                      onChange={() => handleMemberToggle(member.name)}
                    />
                  }
                  label={
                    <Box>
                      <Typography variant='body2'>{member.name}</Typography>
                      <Typography variant='caption' color='text.secondary'>
                        {member.vibe} • {member.location}
                      </Typography>
                    </Box>
                  }
                />
              ))}
            </FormGroup>
          </Grid>

          {/* Analytics Suggestions */}
          {analyticsSuggestions &&
            analyticsSuggestions.suggestions &&
            analyticsSuggestions.suggestions.length > 0 && (
              <Grid item xs={12}>
                <Paper sx={{ p: 3, mt: 3, bgcolor: "grey.50" }}>
                  <Typography
                    variant='h6'
                    gutterBottom
                    sx={{ display: "flex", alignItems: "center" }}>
                    <Lightbulb sx={{ mr: 1, color: "warning.main" }} />
                    AI Suggestions for Better Events
                  </Typography>
                  <Typography
                    variant='body2'
                    color='text.secondary'
                    sx={{ mb: 2 }}>
                    Based on your recent events, here are some insights to
                    improve your team bonding:
                  </Typography>
                  <Grid container spacing={2}>
                    {analyticsSuggestions.suggestions
                      .slice(0, 2)
                      .map((suggestion: any, index: number) => (
                        <Grid item xs={12} md={6} key={index}>
                          <Card variant='outlined' sx={{ p: 2 }}>
                            <Typography
                              variant='subtitle2'
                              color='primary'
                              gutterBottom>
                              {suggestion.title}
                            </Typography>
                            <Typography variant='body2' color='text.secondary'>
                              {suggestion.description}
                            </Typography>
                            <Box
                              sx={{
                                display: "flex",
                                alignItems: "center",
                                mt: 1,
                              }}>
                              <Typography
                                variant='caption'
                                color='text.secondary'>
                                Confidence:{" "}
                                {Math.round(suggestion.confidence * 100)}%
                              </Typography>
                            </Box>
                          </Card>
                        </Grid>
                      ))}
                  </Grid>
                </Paper>
              </Grid>
            )}

          {/* Generate Button */}
          <Grid item xs={12}>
            <Button
              variant='contained'
              size='large'
              onClick={handleGeneratePlans}
              disabled={userPreferences.available_members.length === 0}
              sx={{ mt: 2 }}>
              Generate Event Plans
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {/* Error Display */}
      {error && (
        <Alert severity='error' sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}

      {/* Generated Plans */}
      {plans.length > 0 && (
        <Box sx={{ mt: 4 }}>
          <Typography variant='h5' gutterBottom>
            Generated Plans ({plans.length})
          </Typography>
          <Grid container spacing={3}>
            {plans.map((plan, index) => (
              <Grid item xs={12} md={6} lg={4} key={index}>
                <Card
                  sx={{
                    height: "100%",
                    cursor: "pointer",
                    transition: "transform 0.2s",
                    "&:hover": {
                      transform: "translateY(-4px)",
                    },
                  }}
                  onClick={() => handlePlanClick(plan)}>
                  <CardContent>
                    <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
                      <Box
                        sx={{
                          backgroundColor: getThemeColor(userPreferences.theme),
                          borderRadius: "50%",
                          p: 1,
                          mr: 2,
                        }}>
                        {getThemeIcon(userPreferences.theme)}
                      </Box>
                      <Typography variant='h6'>Plan {index + 1}</Typography>
                    </Box>

                    <Box sx={{ mb: 2 }}>
                      <Typography
                        variant='body2'
                        color='text.secondary'
                        gutterBottom>
                        {plan.fit_analysis}
                      </Typography>
                    </Box>

                    <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
                      <Rating value={plan.rating} readOnly size='small' />
                      <Typography variant='body2' sx={{ ml: 1 }}>
                        {plan.rating}/5
                      </Typography>
                    </Box>

                    <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
                      <AttachMoney sx={{ mr: 1, color: "text.secondary" }} />
                      <Typography variant='body2'>
                        {plan.total_cost.toLocaleString()} VND
                      </Typography>
                    </Box>

                    {plan.contribution_needed > 0 && (
                      <Alert severity='warning' sx={{ mb: 2 }}>
                        Additional contribution:{" "}
                        {plan.contribution_needed.toLocaleString()} VND
                      </Alert>
                    )}

                    <Typography variant='body2' color='text.secondary'>
                      {plan.phases.length} phase
                      {plan.phases.length !== 1 ? "s" : ""}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      )}
    </Container>
  );

  return (
    <Container maxWidth='lg'>
      <Box sx={{ my: 4 }}>
        {/* Main Tabs */}
        <Box sx={{ borderBottom: 1, borderColor: "divider", mb: 3 }}>
          <Tabs
            value={activeTab}
            onChange={(e, newValue) => handleTabChange(newValue)}>
            <Tab label='🎉 Event Planner' />
            <Tab label='👥 Team Members' />
            <Tab label='📅 History' />
            <Tab label='📊 Analytics' />
          </Tabs>
        </Box>

        {/* Tab Content */}
        {activeTab === 0 && renderEventPlanner()}
        {activeTab === 1 && <TeamMemberManagement />}
        {activeTab === 2 && <History />}
        {activeTab === 3 && <AnalyticsSuggestions />}
      </Box>

      {/* Plan Detail Dialog */}
      <Dialog
        open={planDialogOpen}
        onClose={() => setPlanDialogOpen(false)}
        maxWidth='md'
        fullWidth>
        {selectedPlan && (
          <>
            <DialogTitle>
              <Box sx={{ display: "flex", alignItems: "center" }}>
                <Box
                  sx={{
                    backgroundColor: getThemeColor(userPreferences.theme),
                    borderRadius: "50%",
                    p: 1,
                    mr: 2,
                  }}>
                  {getThemeIcon(userPreferences.theme)}
                </Box>
                <Typography variant='h5' sx={{ fontWeight: "bold" }}>
                  Team Bonding Plan
                </Typography>
              </Box>
            </DialogTitle>

            <DialogContent>
              <Grid container spacing={3}>
                <Grid item xs={12} md={8}>
                  <Typography variant='h6' gutterBottom>
                    📍 Event Phases
                  </Typography>

                  {selectedPlan.phases.map(
                    (phase: EventPhase, index: number) => (
                      <Accordion key={index} sx={{ mb: 2 }}>
                        <AccordionSummary expandIcon={<ExpandMore />}>
                          <Box
                            sx={{
                              display: "flex",
                              alignItems: "center",
                              width: "100%",
                            }}>
                            <Typography variant='h6' sx={{ flexGrow: 1 }}>
                              Phase {index + 1}: {phase.activity}
                            </Typography>
                            <Chip
                              label={`${phase.cost.toLocaleString()} VND`}
                              color='primary'
                              size='small'
                            />
                          </Box>
                        </AccordionSummary>

                        <AccordionDetails>
                          <List dense>
                            <ListItem>
                              <ListItemIcon>
                                <LocationOn color='primary' />
                              </ListItemIcon>
                              <ListItemText
                                primary='Address'
                                secondary={phase.location}
                              />
                            </ListItem>

                            {phase.map_link && (
                              <ListItem>
                                <ListItemIcon>
                                  <Directions color='primary' />
                                </ListItemIcon>
                                <ListItemText
                                  primary='Google Maps'
                                  secondary={
                                    <a
                                      href={phase.map_link}
                                      target='_blank'
                                      rel='noopener noreferrer'>
                                      Open in Maps
                                    </a>
                                  }
                                />
                              </ListItem>
                            )}
                          </List>

                          <Box
                            sx={{ display: "flex", gap: 1, flexWrap: "wrap" }}>
                            {phase.indicators.map((indicator, idx) => (
                              <Chip
                                key={idx}
                                label={indicator}
                                size='small'
                                color={
                                  indicator === "indoor"
                                    ? "primary"
                                    : indicator === "outdoor"
                                    ? "secondary"
                                    : indicator === "vegetarian-friendly"
                                    ? "success"
                                    : indicator === "alcohol-friendly"
                                    ? "warning"
                                    : "default"
                                }
                              />
                            ))}
                          </Box>
                        </AccordionDetails>
                      </Accordion>
                    )
                  )}
                </Grid>

                <Grid item xs={12} md={4}>
                  <Paper sx={{ p: 2, mb: 2 }}>
                    <Typography variant='h6' gutterBottom>
                      💰 Cost Breakdown
                    </Typography>
                    <Typography
                      variant='h4'
                      sx={{ color: "#27ae60", fontWeight: "bold" }}>
                      {selectedPlan.total_cost.toLocaleString()} VND
                    </Typography>
                    <Typography variant='body2' sx={{ color: "#7f8c8d" }}>
                      per person
                    </Typography>
                    {selectedPlan.contribution_needed > 0 && (
                      <Alert severity='warning' sx={{ mt: 1 }}>
                        Additional contribution:{" "}
                        {selectedPlan.contribution_needed.toLocaleString()} VND
                      </Alert>
                    )}
                  </Paper>

                  <Paper sx={{ p: 2, mb: 2 }}>
                    <Typography variant='h6' gutterBottom>
                      👥 Team Fit
                    </Typography>
                    <Typography variant='body2' sx={{ color: "#7f8c8d" }}>
                      {selectedPlan.fit_analysis}
                    </Typography>
                    <Box sx={{ display: "flex", alignItems: "center", mt: 1 }}>
                      <Rating
                        value={selectedPlan.rating}
                        readOnly
                        size='small'
                      />
                      <Typography variant='body2' sx={{ ml: 1 }}>
                        {selectedPlan.rating}/5
                      </Typography>
                    </Box>
                  </Paper>
                </Grid>
              </Grid>
            </DialogContent>

            <DialogActions>
              <Button onClick={() => setPlanDialogOpen(false)}>Close</Button>
              <Button
                variant='contained'
                color='primary'
                onClick={handleSavePlan}
                disabled={savingPlan}
                startIcon={savingPlan ? <CircularProgress size={20} /> : null}>
                {savingPlan ? "Saving..." : "Save Plan"}
              </Button>
            </DialogActions>
          </>
        )}
      </Dialog>

      {/* Save Success Dialog */}
      <Dialog
        open={saveSuccessDialogOpen}
        onClose={() => setSaveSuccessDialogOpen(false)}
        maxWidth='sm'
        fullWidth>
        <DialogTitle>
          <Box sx={{ display: "flex", alignItems: "center" }}>
            <Box
              sx={{
                backgroundColor: "#4caf50",
                borderRadius: "50%",
                p: 1,
                mr: 2,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                width: 40,
                height: 40,
              }}>
              <Typography variant='h6' sx={{ color: "white" }}>
                ✓
              </Typography>
            </Box>
            <Typography variant='h6' sx={{ fontWeight: "bold" }}>
              Plan Saved Successfully!
            </Typography>
          </Box>
        </DialogTitle>
        <DialogContent>
          <Typography variant='body1' sx={{ mb: 2 }}>
            Your team bonding plan has been saved to the event history.
          </Typography>
          <Alert severity='info' sx={{ mb: 2 }}>
            <Typography variant='body2'>
              You can now view, edit, or delete this plan from the{" "}
              <strong>History tab</strong>.
            </Typography>
          </Alert>
          <Typography variant='body2' color='text.secondary'>
            The plan includes all phases, costs, and team fit analysis for
            future reference.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSaveSuccessDialogOpen(false)}>Close</Button>
          <Button
            variant='contained'
            color='primary'
            onClick={() => {
              setSaveSuccessDialogOpen(false);
              setActiveTab(2); // Switch to History tab
            }}>
            View in History
          </Button>
        </DialogActions>
      </Dialog>

      {/* Duplicate Detection Dialog */}
      <Dialog
        open={duplicateDialogOpen}
        onClose={() => setDuplicateDialogOpen(false)}
        maxWidth='sm'
        fullWidth>
        <DialogTitle>
          <Box sx={{ display: "flex", alignItems: "center" }}>
            <Box
              sx={{
                backgroundColor: "#ff9800",
                borderRadius: "50%",
                p: 1,
                mr: 2,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                width: 40,
                height: 40,
              }}>
              <Typography variant='h6' sx={{ color: "white" }}>
                ⚠
              </Typography>
            </Box>
            <Typography variant='h6' sx={{ fontWeight: "bold" }}>
              Plan Already Exists
            </Typography>
          </Box>
        </DialogTitle>
        <DialogContent>
          <Typography variant='body1' sx={{ mb: 2 }}>
            A similar plan has already been saved to the event history.
          </Typography>
          <Alert severity='warning' sx={{ mb: 2 }}>
            <Typography variant='body2'>
              This prevents duplicate entries in your history. You can view the
              existing plan in the <strong>History tab</strong>.
            </Typography>
          </Alert>
          <Typography variant='body2' color='text.secondary'>
            If you want to save a different version, try modifying the plan
            details first.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDuplicateDialogOpen(false)}>Close</Button>
          <Button
            variant='contained'
            color='primary'
            onClick={() => {
              setDuplicateDialogOpen(false);
              setActiveTab(2); // Switch to History tab
            }}>
            View in History
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

export default App;
