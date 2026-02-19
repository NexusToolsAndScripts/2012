-- =====================
-- Setup
-- =====================

local service = game.GetService
local cloneref = cloneref or function(Inst) return Inst end
local hui = cloneref((gethui and gethui()) or service(game, "CoreGui").RobloxGui)

local new = Instance.new
local scale = UDim2.fromScale
local color = Color3.new
local udim = UDim.new
local udim2 = UDim2.new
local vector2 = Vector2.new

-- =====================
-- Variables & Functions
-- =====================

local function Center(Inst)
	Inst.AnchorPoint = vector2(0.5, 0.5)
	Inst.Position = scale(0.5, 0.5)
end

local function Stroke(Inst)
	local Str = new("UIStroke")
	Str.Parent = Inst
	Str.ApplyStrokeMode = Enum.ApplyStrokeMode.Border
	
	local Class = {}

	function Class:Color(C)
		Str.Color = C
		return Class
	end

	function Class:Thickness(N)
		Str.Thickness = N
		return Class
	end

	function Class:Transparency(N)
		Str.Transparency = N
		return Class
	end

	return Class
end

local function TextEffect(Inst, Type)
	Inst.TextScaled = true
	Inst.Font = (Type == "Black" and Enum.Font.GothamBlack) or (Type == "Bold" and Enum.Font.GothamBold) or (Type == "Regular" and Enum.Font.Gotham)
	Inst.TextColor3 = color(1, 1, 1)
	Inst.TextStrokeTransparency = 0.5
end

local function Pad(Inst)
	local Padding = new("UIPadding")
	Padding.Parent = Inst

	local Class = {}

	function Class:L(S, O)
		Padding.PaddingLeft = udim(S, O)
		return Class
	end

	function Class:R(S, O)
		Padding.PaddingRight = udim(S, O)
		return Class
	end

	function Class:T(S, O)
		Padding.PaddingTop = udim(S, O)
		return Class
	end

	function Class:B(S, O)
		Padding.PaddingBottom = udim(S, O)
		return Class
	end

	function Class:A(S, O)
		Padding.PaddingLeft = udim(S, O)
		Padding.PaddingRight = udim(S, O)
		Padding.PaddingTop = udim(S, O)
		Padding.PaddingBottom = udim(S, O)
		return Class
	end

	return Class
end

local function Ratio(Inst, X)
	local Constraint = new("UIAspectRatioConstraint")
	Constraint.Parent = Inst
	Constraint.AspectRatio = X or 1
end

-- =====================
-- Services
-- =====================

for _, Name in {} do
	local Get = service(game, Name)
	getfenv()[Name] = cloneref(Get)
end

-- =====================
-- Main
-- =====================

local Library = {}

local Screen = new("ScreenGui")
Screen.Parent = hui
Screen.ResetOnSpawn = false

function Library:Window(Name)
	local Frame = new("Frame")
	Frame.Parent = Screen
	Frame.Size = scale(0.35, 0.35)
	Frame.BorderSizePixel = 0
	Frame.BackgroundTransparency = 0.4
	Frame.BackgroundColor3 = color(0, 0, 0)
	Frame.Active = true
	Frame.Draggable = true
	Center(Frame)
	Stroke(Frame):Color(color(1, 1, 1)):Transparency(0.75)
	Ratio(Frame, 1.75)

	local Title = new("TextLabel")
	Title.Parent = Frame
	Title.Size = scale(1, 0.12)
	Title.BackgroundTransparency = 1
	Title.TextXAlignment = Enum.TextXAlignment.Left
	Title.Text = Name or "Niggaware.ru Leaked Source"
	TextEffect(Title, "Black")
	Pad(Title):A(0.1):L(0.015)

	local TabHolder = new("ScrollingFrame")
	TabHolder.Parent = Frame
	TabHolder.Size = scale(0.2, 0.88)
	TabHolder.AnchorPoint = vector2(0, 1)
	TabHolder.Position = scale(0, 1)
	TabHolder.BackgroundTransparency = 1
	TabHolder.ScrollBarThickness = 0
	TabHolder.AutomaticCanvasSize = Enum.AutomaticSize.Y
	TabHolder.CanvasSize = scale(0, 0)

	local List = new("UIListLayout")
	List.Parent = TabHolder

	local FrameHolder = new("Frame")
	FrameHolder.Parent = Frame
	FrameHolder.Size = scale(0.78, 0.845)
	FrameHolder.Position = scale(0.22, 0.1275)
	FrameHolder.BackgroundTransparency = 1

	local Divider = new("Frame")
	Divider.Parent = Frame
	Divider.Size = udim2(0, 1, 0.82, 0)
	Divider.Position = scale(0.2, 0.14)
	Divider.BorderSizePixel = 0
	Divider.BackgroundTransparency = 0.6

	local Window = {}
	local Tabs = {}

	function Window:Tab(Name)
		local Tab = new("TextButton")
		Tab.Parent = TabHolder
		Tab.Text = Name
		Tab.BackgroundTransparency = 1
		Tab.Size = udim2(1, 0, 0, 40)
		Tab.TextTransparency = 0.3
		TextEffect(Tab, "Bold")
		Pad(Tab):A(0.1, 0)

		local TabFrame = new("ScrollingFrame")
		TabFrame.Parent = FrameHolder
		TabFrame.Size = scale(0.98, 1)
		TabFrame.BackgroundTransparency = 1
		TabFrame.ScrollBarThickness = 6
		TabFrame.ScrollBarImageTransparency = 0.5
		TabFrame.AutomaticCanvasSize = Enum.AutomaticSize.Y
		TabFrame.CanvasSize = scale(0, 0)

		local List = new("UIListLayout")
		List.Parent = TabFrame
		List.SortOrder = Enum.SortOrder.LayoutOrder
		List.Padding = udim(0, 5)

		local Selected = #Tabs == 0
		TabFrame.Visible = Selected
		Tab.TextTransparency = Selected and 0.3 or 0.7

		table.insert(Tabs, {Tab, TabFrame, Selected})

		Tab.MouseEnter:Connect(function()
			for _, T in Tabs do
				if T[1] == Tab then
					Tab.TextTransparency = T[3] and 0.3 or 0.5
				end
			end
		end)

		Tab.MouseLeave:Connect(function()
			for _, T in Tabs do
				if T[1] == Tab then
					Tab.TextTransparency = T[3] and 0.3 or 0.7
				end
			end
		end)

		Tab.MouseButton1Down:Connect(function()
			for _, T in Tabs do
				local isSelf = (T[2] == TabFrame)
				T[2].Visible = isSelf

				if isSelf then
					T[3] = true
				else
					T[3] = false
				end
			end
		end)

		local TabClass = {}
		local SectionCount = 0
		
		function TabClass:Section(Name)
			SectionCount += 1
			local Section = new("Frame")
			Section.Parent = TabFrame
			Section.Size = scale(1, 0)
			Section.AutomaticSize = Enum.AutomaticSize.Y
			Section.BackgroundColor3 = color(1, 1, 1)
			Section.BackgroundTransparency = 0.9
			Section.LayoutOrder = SectionCount * 2
			Pad(Section):A(0, 5)

			local List = new("UIListLayout")
			List.Parent = Section
			List.SortOrder = Enum.SortOrder.LayoutOrder
			List.Padding = udim(0, 5)

			if Name then
				local Title = new("TextLabel")
				Title.Parent = TabFrame
				Title.Text = Name
				Title.BackgroundTransparency = 0.7
				Title.Size = udim2(1, 0, 0, 40)
				Title.LayoutOrder = (SectionCount * 2) - 1
				Title.BorderSizePixel = 0
				TextEffect(Title, "Black")
				Pad(Title):A(0.1, 0)
			end

			local SectionClass = {}

			function SectionClass:Button(Name, Callback)
				local Button = new("TextButton")
				Button.Parent = Section
				Button.Size = udim2(1, 0, 0, 30)
				Button.BackgroundColor3 = color(0, 0, 0)
				Button.BackgroundTransparency = 0.5
				Button.Text = Name
				Button.BorderSizePixel = 0
				TextEffect(Button, "Bold")
				Pad(Button):A(0.1, 0)

				Button.MouseEnter:Connect(function()
					Button.BackgroundTransparency = 0.8
				end)

				Button.MouseLeave:Connect(function()
					Button.BackgroundTransparency = 0.5
				end)

				Button.MouseButton1Down:Connect(Callback)
			end

			function SectionClass:TextBox(Name, Callback)
				local Box = new("TextBox")
				Box.Parent = Section
				Box.Size = udim2(1, 0, 0, 30)
				Box.BackgroundColor3 = color(0, 0, 0)
				Box.BackgroundTransparency = 0.5
				Box.PlaceholderText = Name
				Box.Text = ""
				Box.BorderSizePixel = 0
				TextEffect(Box, "Bold")
				Pad(Box):A(0.1, 0)

				Box.FocusLost:Connect(function()
					Callback(Box.Text)
				end)
			end

			function SectionClass:Toggle(Name, Callback)
				local ToggleFrame = new("Frame")
				ToggleFrame.Parent = Section
				ToggleFrame.Size = udim2(1, 0, 0, 30)
				ToggleFrame.BackgroundTransparency = 0.7
				ToggleFrame.BackgroundColor3 = color(0, 0, 0)
				ToggleFrame.BorderSizePixel = 0
				Pad(ToggleFrame):A(0.1):L(0.02):R(0.02)

				local List = new("UIListLayout")
				List.Parent = ToggleFrame
				List.FillDirection = Enum.FillDirection.Horizontal
				List.SortOrder = Enum.SortOrder.LayoutOrder
				List.HorizontalFlex = Enum.UIFlexAlignment.SpaceBetween

				local ToggleTitle = new("TextLabel")
				ToggleTitle.Parent = ToggleFrame
				ToggleTitle.Size = udim2(0.5, 0, 1, 0)
				ToggleTitle.BackgroundTransparency = 1
				ToggleTitle.Text = Name
				ToggleTitle.TextXAlignment = Enum.TextXAlignment.Left
				TextEffect(ToggleTitle, "Bold")

				local ToggleButton = new("ImageButton")
				ToggleButton.Parent = ToggleFrame
				ToggleButton.Size = udim2(0.5, 0, 1, 0)
				ToggleButton.BackgroundTransparency = 0.8
				ToggleButton.Image = ""
				ToggleButton.BackgroundColor3 = color(0, 0, 0)
				ToggleButton.ImageTransparency = 0.5
				ToggleButton.BorderSizePixel = 0
				Pad(ToggleButton):A(0.1):L(0.02)
				Ratio(ToggleButton)
				Stroke(ToggleButton):Color(color(1, 1, 1)):Transparency(0.9)

				ToggleButton.MouseEnter:Connect(function()
					ToggleButton.BackgroundTransparency = 0.5
				end)

				ToggleButton.MouseLeave:Connect(function()
					ToggleButton.BackgroundTransparency = 0.8
				end)

				local Toggle = false
				ToggleButton.MouseButton1Down:Connect(function()
					Toggle = not Toggle
					ToggleButton.Image = Toggle and "rbxassetid://8589545938" or ""
					Callback(Toggle)
				end)
			end

			function SectionClass:Dropdown(Name, Options, Callback)
				local Holder = new("Frame")
				Holder.Parent = Section
				Holder.Size = udim2(1, 0, 0, 30)
				Holder.BackgroundTransparency = 0.7
				Holder.BackgroundColor3 = color(0, 0, 0)
				Pad(Holder):A(0.1):L(0.02):R(0.02)

				local Title = new("TextLabel")
				Title.Parent = Holder
				Title.Size = udim2(0.5, 0, 1, 0)
				Title.BackgroundTransparency = 1
				Title.Text = Name
				Title.TextXAlignment = Enum.TextXAlignment.Left
				TextEffect(Title, "Bold")

				local Selected = Options[1]
				local Button = new("TextButton")
				Button.Parent = Holder
				Button.Size = udim2(0.5, 0, 1, 0)
				Button.Position = scale(0.5, 0)
				Button.BackgroundColor3 = color(0, 0, 0)
				Button.BackgroundTransparency = 0.5
				Button.Text = Selected
				Button.BorderSizePixel = 0
				TextEffect(Button, "Bold")

				local Dropped = false
				local OptionButtons = {}
				for _, Option in ipairs(Options) do
					local C = Button:Clone()
					C.Parent = Button
					C.Text = Option
					C.Visible = false
					OptionButtons[_] = C

					if _ == 1 then
						C.Visible = false
					end

					C.MouseEnter:Connect(function()
						C.BackgroundTransparency = 0.8
					end)

					C.MouseLeave:Connect(function()
						C.BackgroundTransparency = 0.5
					end)

					C.MouseButton1Down:Connect(function()
						Button.Text = Option
						Callback(Option)
						Selected = Option
						
						for _, B in OptionButtons do
							B.Visible = false
						end

						Dropped = false
					end)
				end

				Button.MouseEnter:Connect(function()
					Button.BackgroundTransparency = 0.8
				end)

				Button.MouseLeave:Connect(function()
					Button.BackgroundTransparency = 0.5
				end)

				Button.MouseButton1Down:Connect(function()
					if Dropped then
						for _, B in ipairs(OptionButtons) do
							B.Visible = false
						end
						Dropped = false
						return
					end

					local C = 0
					for _, B in ipairs(OptionButtons) do
						B.Visible = Options[_] ~= Selected
						if B.Visible then
							C += 1
						end
						B.Position = scale(0, C)
						B.Size = scale(1, 1)
					end
					Dropped = true
				end)
			end

			return SectionClass
		end

		return TabClass
	end

	return Window
end

return Library
