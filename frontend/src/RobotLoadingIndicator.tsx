import React from 'react';
import { Bot } from 'lucide-react';

const RobotLoadingIndicator: React.FC = () => {
  return (
    <div className="w-full flex flex-col items-center justify-center space-y-4 my-8">
      {/* Progress Bar Container */}
      <div className="w-3/4 relative h-8">
        {/* The track for the robot */}
        <div className="h-2 bg-muted rounded-full absolute top-1/2 -translate-y-1/2 w-full"></div>
        {/* The animated robot icon */}
        <div className="absolute top-0" style={{ animation: 'robot-run 4s ease-in-out infinite' }}>
          <Bot className="w-8 h-8 text-primary" />
        </div>
      </div>

      <h3 className="text-lg font-semibold text-foreground animate-pulse">
        Our AI is building your perfect event...
      </h3>
      <p className="text-sm text-muted-foreground">
        Please wait a moment.
      </p>

      {/* Keyframes for the animation, scoped to this component */}
      <style>{`
        @keyframes robot-run {
          0% { left: 0%; }
          50% { left: calc(100% - 2rem); } /* 2rem is w-8 */
          100% { left: 0%; }
        }
      `}</style>
    </div>
  );
};

export default RobotLoadingIndicator; 