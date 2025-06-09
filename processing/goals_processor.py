# processing/goals_processor.py
class GoalsProcessor:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_new_goal(self, user_id, goal_data):
        if not goal_data.get('goal_name') or not goal_data.get('deadline'):
            return False, "Goal name and deadline are required."
        if not goal_data.get('target_revenue') and not goal_data.get('target_quantity'):
            return False, "You must set a target for either revenue or quantity."
        
        return self.db_manager.add_goal(user_id, goal_data)

    def get_all_goals_with_progress(self, user_id):
        goals = self.db_manager.get_user_goals(user_id)
        
        for goal in goals:
            progress = self.db_manager.get_sales_progress_for_goal(
                user_id,
                goal['start_date'],
                goal['deadline'],
                goal.get('product_id')
            )
            goal['current_revenue'] = progress['total_revenue']
            goal['current_quantity'] = progress['total_quantity']
        
        return goals
    
    def delete_goal(self, user_id, goal_id):
        return self.db_manager.delete_goal(goal_id, user_id)