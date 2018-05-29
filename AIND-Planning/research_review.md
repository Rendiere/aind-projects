# Historical Developments of Planning

In this report, we will outline the history of planning as a component of AI research by considering three influential developments.

The first of these is **Shakey the Robot** [cite], the first robot to incorporate AI. Shakey was developed by the Stanford Research Institute (SRI) and took 8 years to build from start to finish (1966 - 1972). This was the first time that multiple cutting edge technologies in the fields of television (computer vision), robotics and computer science were combined into one "automaton". Shakey was designed using the _STRIPS_ problem solver [1]. _STRIPS_, as a solver boils down to using already defined strategies such a General Problem Solving (GPS), but with a very specific way of defining the problem. This way of defining the problem, was adopted as a new planning _language_.

The STRIPS language sets some rules for defining the planning project. To adhere to these rules, each problem needs to have:
* _1) An initial state_
* _2) A set of possible actions, each with their own pre- and post conditions_, and
* _3) A goal state._

Thus, it is clear that Part 1 of this project (`my_cargo_planner`) adheres to the rules of and thus was written in STRIPS and that Problem Domain Description Language (PPDL) is basically STRIPS that is computer parseable and with a standardized syntax.


More than 20 years later, a significant improvement on STRIPS came in the form of the _Graphplan_ planner [2]. _Graphplan_ introduced the concept of a _planning graph_, such as the one implemented in Part 2 of this project. The input to the _Graphplan_ planner is a problem defined in the STRIPS language, form which it constructs a planning graph. The solution provided will always be the shortest possible partial order plan, or else _Graphplan_ will state that no valid plan exists.
_Graphplan_ was a distinct deviation from the major trend of the time - partial order planning (POP). It proved to be a significant improvement on state of the art POP based systems, and soon after it's introduction various other _planning graph_ based planners emerged [3,4]

In the early 2000's however, Nguyen and Kambhampati aimed to revitalize the dwindling interest in POP, which was seen as poorly scalable after the introduction of _planning graphs_. They introduced a new planner (aptly) name _RePOP_ [5], which improved on the _planning graph_ based solvers by adding the missing efficiency and flexibility when solving parallel planning domains. _RePOP_ is based on _UCPOP_ [6], a successful POP solver, but drastically improved in terms of efficiency by, amongst other things presenting new ways of adapting distance based heuristics. _RePOP_ was a significant overhaul of how POP solvers were designed at the time and definitely a noteworthy contribution to the field of planning and AI.

### References

* [1] R.E Fikes and N.J Nilsson: STRIPS: A New Approach to the Application of Theorem Proving to Problem Solving. _Artificial Intelligence 2 (1971), 189--208_
* [2] A.L Blum and M. L Furst: Fast Planning Through Planning Graph Analysis. _Artificial Intelligence, 90:281–300, 1997_
* [3] Fox, M. S. and Long, D. (1998). The automatic in- ference of state invariants in TIM. _JAIR, 9, 367–421_.
* [4] Koehler, J., Nebel, B., Hoffmann, J., and Dimopou- los, Y. (1997). Extending planning graphs to an ADL subset. _In ECP-97, pp. 273–285._
* [5] Nguyen, X. and Kambhampati, S. (2001). Reviving partial order planning. _In IJCAI-01, pp. 459–466._
* [6] D. Weld. An introduction to least commitment planning. _AI
magazine, 1994._
