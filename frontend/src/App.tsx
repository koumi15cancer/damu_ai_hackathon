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
  IconButton,
  Avatar,
  AvatarGroup,
  Container,
  Box,
  Grid,
  Paper,
  Typography,
  TextField,
  FormControl,
  FormGroup,
  DialogActions,
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
import { Badge } from "./components/ui/badge";
import { Alert, AlertDescription, AlertTitle } from "./components/ui/alert";
import RobotLoadingIndicator from "./RobotLoadingIndicator";

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
    theme: "none",
    budget_contribution: "No",
    available_members: [],
    date_time: "",
    location_zone: "",
    ai_model: "",
    plan_generation_mode: "new",
  });

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
        theme: userPreferences.theme === "none" ? "" : userPreferences.theme,
        ai_model: userPreferences.ai_model,
        plan_generation_mode: userPreferences.plan_generation_mode,
      };

      const response = await axios.post(
        "http://localhost:5000/generate-plans",
        requestData
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
        theme: userPreferences.theme === "none" ? "" : userPreferences.theme,
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

      // Close the dialog and show success message
      setPlanDialogOpen(false);
      setSelectedPlan(null);
      setSaveSuccessDialogOpen(true);
    } catch (error: any) {
      console.error("Failed to save plan:", error);

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
      case "none":
        return <Group />;
      default:
        return <Group />;
    }
  };

  const renderEventPlanner = () => (
    <div className='space-y-6'>
      <div className='text-center'>
        <h1 className='text-3xl font-bold text-foreground'>
          Team Bonding Event Planner
        </h1>
        <p className='text-muted-foreground'>
          Generate personalized team bonding plans based on member preferences
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Event Preferences</CardTitle>
        </CardHeader>
        <CardContent className='space-y-4'>
          <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
            <div>
              <Label>Event Theme</Label>
              <Select
                value={userPreferences.theme}
                onValueChange={(value: string) =>
                  setUserPreferences((prev) => ({ ...prev, theme: value }))
                }>
                <SelectTrigger>
                  <SelectValue placeholder='Select a theme' />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value='none'>No specific theme</SelectItem>
                  <SelectItem value='fun 🎉'>Fun 🎉</SelectItem>
                  <SelectItem value='chill 🧘'>Chill 🧘</SelectItem>
                  <SelectItem value='outdoor 🌤'>Outdoor 🌤</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Budget Contribution</Label>
              <Select
                value={userPreferences.budget_contribution}
                onValueChange={(value: string) =>
                  setUserPreferences((prev) => ({
                    ...prev,
                    budget_contribution: value,
                  }))
                }>
                <SelectTrigger>
                  <SelectValue placeholder='Select budget' />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value='No'>No additional contribution</SelectItem>
                  <SelectItem value='Yes, up to 50,000 VND'>
                    Yes, up to 50,000 VND
                  </SelectItem>
                  <SelectItem value='Yes, up to 100,000 VND'>
                    Yes, up to 100,000 VND
                  </SelectItem>
                  <SelectItem value='Yes, up to 150,000 VND'>
                    Yes, up to 150,000 VND
                  </SelectItem>
                  <SelectItem value='Yes, up to 200,000 VND'>
                    Yes, up to 200,000 VND
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
            <div>
              <Label>Preferred Date & Time</Label>
              <Input
                type='datetime-local'
                value={userPreferences.date_time}
                onChange={(e) =>
                  setUserPreferences((prev: UserPreferences) => ({
                    ...prev,
                    date_time: e.target.value,
                  }))
                }
              />
            </div>
            <div>
              <Label>Preferred Location Zone</Label>
              <Input
                placeholder='e.g., District 1'
                value={userPreferences.location_zone}
                onChange={(e) =>
                  setUserPreferences((prev: UserPreferences) => ({
                    ...prev,
                    location_zone: e.target.value,
                  }))
                }
              />
            </div>
          </div>

          {availableAIModels.length > 0 && (
            <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
              <div>
                <Label>AI Model</Label>
                <Select
                  value={userPreferences.ai_model || ""}
                  onValueChange={(value: string) =>
                    setUserPreferences((prev) => ({
                      ...prev,
                      ai_model: value,
                    }))
                  }>
                  <SelectTrigger>
                    <SelectValue placeholder='Select AI model' />
                  </SelectTrigger>
                  <SelectContent>
                    {availableAIModels.map((model) => (
                      <SelectItem key={model} value={model}>
                        {model}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label>Plan Generation Mode</Label>
                <Select
                  value={userPreferences.plan_generation_mode || "new"}
                  onValueChange={(value: string) =>
                    setUserPreferences((prev) => ({
                      ...prev,
                      plan_generation_mode: value,
                    }))
                  }>
                  <SelectTrigger>
                    <SelectValue placeholder='Select mode' />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value='new'>Generate New Plans</SelectItem>
                    <SelectItem value='reuse'>Reuse Previous Plans</SelectItem>
                    <SelectItem value='hybrid'>Hybrid Approach</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          )}

          <div>
            <h3 className='text-lg font-medium text-foreground mb-2'>
              Available Team Members
            </h3>
            <div className='grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4'>
              {teamMembers.map((member) => (
                <div key={member.id} className='flex items-center space-x-2'>
                  <Checkbox
                    id={member.id}
                    checked={userPreferences.available_members.includes(
                      member.name
                    )}
                    onCheckedChange={() => handleMemberToggle(member.name)}
                  />
                  <Label
                    htmlFor={member.id}
                    className='text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70'>
                    <span className='block'>{member.name}</span>
                    <span className='text-xs text-muted-foreground'>
                      {member.vibe} • {member.location}
                    </span>
                  </Label>
                </div>
              ))}
            </div>
          </div>

          <Button
            onClick={handleGeneratePlans}
            disabled={userPreferences.available_members.length === 0 || loading}
            className='w-full'>
            {loading ? (
              <>
                <CircularProgress size={20} className='mr-2' />
                Generating Plans...
              </>
            ) : (
              "Generate Event Plans"
            )}
          </Button>

          {/* Analytics Suggestions */}
          {analyticsSuggestions &&
            analyticsSuggestions.suggestions &&
            analyticsSuggestions.suggestions.length > 0 && (
              <div className='mt-6 p-4 bg-gray-50 rounded-lg'>
                <div className='flex items-center mb-3'>
                  <Lightbulb className='mr-2 text-yellow-600' />
                  <h4 className='text-lg font-semibold'>
                    AI Suggestions for Better Events
                  </h4>
                </div>
                <p className='text-sm text-gray-600 mb-4'>
                  Based on your recent events, here are some insights to improve
                  your team bonding:
                </p>
                <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
                  {analyticsSuggestions.suggestions
                    .slice(0, 2)
                    .map((suggestion: any, index: number) => (
                      <Card key={index} className='p-3'>
                        <h5 className='font-medium text-blue-600 mb-1'>
                          {suggestion.title}
                        </h5>
                        <p className='text-sm text-gray-600 mb-2'>
                          {suggestion.description}
                        </p>
                        <div className='flex items-center'>
                          <span className='text-xs text-gray-500'>
                            Confidence:{" "}
                            {Math.round(suggestion.confidence * 100)}%
                          </span>
                        </div>
                      </Card>
                    ))}
                </div>
              </div>
            )}
        </CardContent>
      </Card>

      {loading ? (
        <RobotLoadingIndicator />
      ) : (
        <>
          {error && (
            <Alert variant='destructive'>
              <AlertTitle>Error</AlertTitle>
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {plans.length > 0 && (
            <div>
              <h2 className='text-2xl font-bold text-foreground mb-4'>
                Generated Plans ({plans.length})
              </h2>
              <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'>
                {plans.map((plan, index) => (
                  <Card
                    key={index}
                    className='cursor-pointer transition-transform hover:-translate-y-1'
                    onClick={() => handlePlanClick(plan)}>
                    <CardHeader>
                      <CardTitle className='flex items-center'>
                        <div className='p-2 mr-3 bg-primary/10 rounded-full text-primary'>
                          {getThemeIcon(userPreferences.theme)}
                        </div>
                        Plan {index + 1}
                      </CardTitle>
                    </CardHeader>
                    <CardContent className='space-y-3'>
                      <p className='text-sm text-muted-foreground'>
                        {plan.fit_analysis}
                      </p>
                      <div className='flex items-center'>
                        <Rating value={plan.rating} readOnly size='small' />
                        <span className='text-sm ml-2'>{plan.rating}/5</span>
                      </div>
                      <div className='flex items-center text-muted-foreground'>
                        <AttachMoney fontSize='small' className='mr-1' />
                        <span className='text-sm'>
                          {plan.total_cost.toLocaleString()} VND
                        </span>
                      </div>
                      {plan.contribution_needed > 0 && (
                        <Alert variant='warning' className='mt-2'>
                          <AlertDescription>
                            Additional contribution:{" "}
                            {plan.contribution_needed.toLocaleString()} VND
                          </AlertDescription>
                        </Alert>
                      )}
                      <p className='text-sm text-muted-foreground'>
                        {plan.phases.length} phase
                        {plan.phases.length !== 1 ? "s" : ""}
                      </p>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );

  return (
    <Container maxWidth='lg'>
      <Box sx={{ my: 4 }}>
        {/* Main Tabs */}
        <Tabs
          value={activeTab.toString()}
          onValueChange={(value) => handleTabChange(parseInt(value))}>
          <TabsList className='grid w-full grid-cols-4'>
            <TabsTrigger value='0'>🎉 Event Planner</TabsTrigger>
            <TabsTrigger value='1'>👥 Team Members</TabsTrigger>
            <TabsTrigger value='2'>📅 History</TabsTrigger>
            <TabsTrigger value='3'>📊 Analytics</TabsTrigger>
          </TabsList>

          {/* Tab Content */}
          <TabsContent value='0' className='mt-6'>
            {renderEventPlanner()}
          </TabsContent>
          <TabsContent value='1' className='mt-6'>
            <TeamMemberManagement />
          </TabsContent>
          <TabsContent value='2' className='mt-6'>
            <History />
          </TabsContent>
          <TabsContent value='3' className='mt-6'>
            <AnalyticsSuggestions />
          </TabsContent>
        </Tabs>
      </Box>

      {/* Plan Detail Dialog */}
      <Dialog open={planDialogOpen} onOpenChange={setPlanDialogOpen}>
        <DialogContent className='max-w-3xl'>
          {selectedPlan && (
            <>
              <DialogHeader>
                <DialogTitle className='flex items-center'>
                  <div className='p-2 mr-3 bg-primary/10 rounded-full text-primary'>
                    {getThemeIcon(userPreferences.theme)}
                  </div>
                  <span className='text-2xl font-bold'>Team Bonding Plan</span>
                </DialogTitle>
              </DialogHeader>

              <div className='grid md:grid-cols-3 gap-6 py-4'>
                <div className='md:col-span-2 space-y-3'>
                  <h3 className='text-lg font-semibold'>📍 Event Phases</h3>
                  {selectedPlan.phases.map(
                    (phase: EventPhase, index: number) => (
                      <Accordion key={index} sx={{ mb: 2 }}>
                        <AccordionSummary expandIcon={<ExpandMore />}>
                          <div className='flex justify-between items-center w-full'>
                            <h4 className='font-semibold'>
                              Phase {index + 1}: {phase.activity}
                            </h4>
                            <Badge variant='secondary'>
                              {phase.cost.toLocaleString()} VND
                            </Badge>
                          </div>
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
                                      rel='noopener noreferrer'
                                      className='text-blue-500 hover:underline'>
                                      Open in Maps
                                    </a>
                                  }
                                />
                              </ListItem>
                            )}
                          </List>
                          <div className='flex gap-2 flex-wrap'>
                            {phase.indicators.map((indicator, idx) => (
                              <Badge key={idx} variant='secondary'>
                                {indicator}
                              </Badge>
                            ))}
                          </div>
                        </AccordionDetails>
                      </Accordion>
                    )
                  )}
                </div>

                <div className='space-y-4'>
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
                      <Alert variant='destructive' className='mt-2'>
                        <AlertDescription>
                          Additional contribution:{" "}
                          {selectedPlan.contribution_needed.toLocaleString()}{" "}
                          VND
                        </AlertDescription>
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
                </div>
              </div>
            </>
          )}
          <DialogFooter>
            <Button onClick={() => setPlanDialogOpen(false)}>Close</Button>
            <Button onClick={handleSavePlan} disabled={savingPlan}>
              {savingPlan ? (
                <>
                  <CircularProgress size={20} className='mr-2' />
                  Saving...
                </>
              ) : (
                "Save Plan"
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Success Dialog */}
      <Dialog
        open={saveSuccessDialogOpen}
        onOpenChange={setSaveSuccessDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className='flex items-center'>
              <div className='w-10 h-10 bg-green-500 rounded-full flex items-center justify-center mr-3'>
                <span className='text-white font-bold'>✓</span>
              </div>
              <span className='text-xl font-bold'>
                Plan Saved Successfully!
              </span>
            </DialogTitle>
          </DialogHeader>
          <div className='py-4'>
            <p className='mb-4'>
              Your team bonding plan has been saved to the event history.
            </p>
            <Alert>
              <AlertDescription>
                You can now view, edit, or delete this plan from the{" "}
                <strong>History tab</strong>.
              </AlertDescription>
            </Alert>
            <p className='text-sm text-gray-600 mt-4'>
              The plan includes all phases, costs, and team fit analysis for
              future reference.
            </p>
          </div>
          <DialogFooter>
            <Button onClick={() => setSaveSuccessDialogOpen(false)}>
              Close
            </Button>
            <Button
              onClick={() => {
                setSaveSuccessDialogOpen(false);
                setActiveTab(2); // Switch to History tab
              }}>
              View in History
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Duplicate Detection Dialog */}
      <Dialog open={duplicateDialogOpen} onOpenChange={setDuplicateDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className='flex items-center'>
              <div className='w-10 h-10 bg-orange-500 rounded-full flex items-center justify-center mr-3'>
                <span className='text-white font-bold'>⚠</span>
              </div>
              <span className='text-xl font-bold'>Plan Already Exists</span>
            </DialogTitle>
          </DialogHeader>
          <div className='py-4'>
            <p className='mb-4'>
              A similar plan has already been saved to the event history.
            </p>
            <Alert variant='destructive'>
              <AlertDescription>
                This prevents duplicate entries in your history. You can view
                the existing plan in the <strong>History tab</strong>.
              </AlertDescription>
            </Alert>
            <p className='text-sm text-gray-600 mt-4'>
              If you want to save a different version, try modifying the plan
              details first.
            </p>
          </div>
          <DialogFooter>
            <Button onClick={() => setDuplicateDialogOpen(false)}>Close</Button>
            <Button
              onClick={() => {
                setDuplicateDialogOpen(false);
                setActiveTab(2); // Switch to History tab
              }}>
              View in History
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </Container>
  );
}

export default App;
