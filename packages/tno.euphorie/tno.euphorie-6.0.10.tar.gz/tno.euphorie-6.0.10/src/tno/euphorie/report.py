# coding=utf-8
from euphorie.client import MessageFactory as eu_
from euphorie.client import model
from euphorie.client.report import ActionPlanReportDownload
from euphorie.client.report import createSection
from euphorie.client.report import MeasuresOverview
from euphorie.client.report import ReportLanding
# from euphorie.client.report import RisksOverview
from euphorie.ghost import PathGhost
from five import grok
from plonetheme.nuplone.utils import formatDate
from rtfng.document.paragraph import Cell
from rtfng.document.paragraph import Paragraph
from rtfng.document.paragraph import Table
from rtfng.PropertySets import TabPropertySet
from sqlalchemy import sql
from tno.euphorie.company import DutchCompanySchema
from tno.euphorie.interfaces import ITnoReportPhaseSkinLayer
from tno.euphorie.model import DutchCompany
from z3c.saconfig import Session
from zope.i18n import translate
from euphorie.client.session import SessionManager
from datetime import date
from zope.i18nmessageid import MessageFactory
from collections import defaultdict
from euphorie.content.interfaces import ICustomRisksModule
from euphorie.content.profilequestion import IProfileQuestion

PloneLocalesFactory = MessageFactory("plonelocales")

grok.templatedir("templates")


def formatAddress(address, postal, city):
    output=[]
    if address:
        output.append(address)
        if postal or city:
            output.append(u"\n")
    bits=filter(None, [postal, city])
    if bits:
        output.append(u" ".join(bits))
    return u"".join(output) if output else None


class TNOReportLanding(ReportLanding):
    """Custom report landing page.

    This replaces the standard online view of the report with a page
    offering the RTF and XLSX download options.
    """
    grok.context(PathGhost)
    grok.layer(ITnoReportPhaseSkinLayer)
    grok.template("report_landing")


class TnoActionPlanReportDownload(ActionPlanReportDownload):
    grok.layer(ITnoReportPhaseSkinLayer)
    grok.name("download")

    def getNodes(self):
        query = Session.query(model.SurveyTreeItem)\
                .filter(model.SurveyTreeItem.session == self.session)\
                .filter(sql.not_(model.SKIPPED_PARENTS))\
                .filter(sql.or_(model.MODULE_WITH_RISK_OR_TOP5_FILTER,
                                model.RISK_PRESENT_OR_TOP5_FILTER))\
                .order_by(model.SurveyTreeItem.path)
        return  query.all()

    def update(self):
        super(TnoActionPlanReportDownload, self).update()
        if self.session.dutch_company is None:
            self.session.dutch_company=DutchCompany()

    def addCompanyInformation(self, document):
        request=self.request
        company=self.session.dutch_company
        t=lambda txt: translate(txt, context=request)
        section = createSection(document, self.context, self.session,
                self.request)
        normal_style=document.StyleSheet.ParagraphStyles.Normal
        missing=t(eu_("missing_data", default=u"Not provided"))

        section.append(Paragraph(
            document.StyleSheet.ParagraphStyles.Heading1,
            t(eu_("plan_report_company_header", default=u"Company details"))))

        table=Table(TabPropertySet.DEFAULT_WIDTH*3, TabPropertySet.DEFAULT_WIDTH*8)

        field=DutchCompanySchema["title"]
        table.append(
                Cell(Paragraph(normal_style, str(field.title))),
                Cell(Paragraph(normal_style, company.title if company.title else missing)))

        address=formatAddress(company.address_visit_address,
                company.address_visit_postal, company.address_visit_city)
        table.append(
                Cell(Paragraph(normal_style, "Bezoekadres bedrijf")),
                Cell(Paragraph(normal_style, address if address else missing)))

        address=formatAddress(company.address_postal_address,
                company.address_postal_postal, company.address_postal_city)
        table.append(
                Cell(Paragraph(normal_style, "Postadres bedrijf")),
                Cell(Paragraph(normal_style, address if address else missing)))

        for key in ["email", "phone", "activity", "submitter_name",
                      "submitter_function", "department", "location"]:
            field=DutchCompanySchema[key]
            value=getattr(company, key, None)
            table.append(
                    Cell(Paragraph(normal_style, field.title)),
                    Cell(Paragraph(normal_style, value if value else missing))),

        formatDecimal=request.locale.numbers.getFormatter("decimal").format
        field=DutchCompanySchema["absentee_percentage"]
        table.append(
                Cell(Paragraph(normal_style, field.title)),
                Cell(Paragraph(normal_style, u"%s %%" % formatDecimal(company.absentee_percentage) if company.absentee_percentage else missing)))

        for key in [ "accidents", "incapacitated_workers"]:
            field=DutchCompanySchema[key]
            value=getattr(company, key, None)
            table.append(
                    Cell(Paragraph(normal_style, field.title)),
                    Cell(Paragraph(normal_style, "%d" % value if value is not None else missing)))

        field=DutchCompanySchema["submit_date"]
        table.append(
                Cell(Paragraph(normal_style, field.title)),
                Cell(Paragraph(normal_style, formatDate(request, company.submit_date) if company.submit_date else missing)))

        field=DutchCompanySchema["employees"]
        table.append(
                Cell(Paragraph(normal_style, field.title)),
                Cell(Paragraph(normal_style, field.vocabulary.getTerm(company.employees).title if company.employees else missing)))

        field=DutchCompanySchema["arbo_expert"]
        table.append(
                Cell(Paragraph(normal_style, str(field.title))),
                Cell(Paragraph(normal_style, company.arbo_expert if company.arbo_expert else missing)))

        section.append(table)


# class TNORisksOverview(RisksOverview):
#     """ Implements the "Overview of Risks" report, see #10967
#     """
#     grok.layer(ITnoReportPhaseSkinLayer)
#     grok.template("risks_overview")
#     grok.name("risks_overview")

#     def update(self):
#         self.session = SessionManager.session
#         if (
#             self.session is not None and self.session.title != (
#                 callable(getattr(self.context, 'Title', None)) and
#                 self.context.Title() or ''
#             )
#         ):
#             self.session_title = self.session.title
#         else:
#             self.session_title = (
#                 callable(getattr(self.context, 'Title', None)) and
#                 self.context.Title() or '')
#         self.getStatus()


class TNOMeasuresOverview(MeasuresOverview):
    """ Implements the "Overview of Measures" report, see #10967
    """
    grok.layer(ITnoReportPhaseSkinLayer)
    grok.template("measures_overview")
    grok.name("measures_overview")

    def update(self):
        self.session = SessionManager.session
        lang = getattr(self.request, 'LANGUAGE', 'en')
        if "-" in lang:
            lang = lang.split("-")[0]
        if (
            self.session is not None and self.session.title != (
                callable(getattr(self.context, 'Title', None)) and
                self.context.Title() or ''
            )
        ):
            self.session_title = self.session.title
        else:
            self.session_title = (
                callable(getattr(self.context, 'Title', None)) and
                self.context.Title() or '')
        today = date.today()
        next_month = date(today.year, (today.month + 1) % 12 or 12, 1)
        month_after_next = date(today.year, (today.month + 2) % 12 or 12, 1)
        self.months = []
        self.months.append(today.strftime('%b'))
        self.months.append(next_month.strftime('%b'))
        self.months.append(month_after_next.strftime('%b'))
        self.monthstrings = [
            translate(
                PloneLocalesFactory(
                    "month_{0}_abbr".format(month.lower()),
                    default=month,
                ),
                target_language=lang,
            )
            for month in self.months
        ]

        query = Session.query(model.Module, model.Risk, model.ActionPlan)\
            .filter(sql.and_(model.Module.session == self.session,
                             model.Module.profile_index > -1))\
            .filter(sql.not_(model.SKIPPED_PARENTS))\
            .filter(sql.or_(model.MODULE_WITH_RISK_OR_TOP5_FILTER,
                            model.RISK_PRESENT_OR_TOP5_FILTER))\
            .join((model.Risk,
                   sql.and_(model.Risk.path.startswith(model.Module.path),
                            model.Risk.depth == model.Module.depth+1,
                            model.Risk.session == self.session)))\
            .join((model.ActionPlan,
                   model.ActionPlan.risk_id == model.Risk.id))\
            .order_by(
                sql.case(
                    value=model.Risk.priority,
                    whens={'high': 0, 'medium': 1},
                    else_=2),
                model.Risk.path)
        measures = [t for t in query.all() if (
            (
                (t[-1].planning_start is not None and
                    t[-1].planning_start.strftime('%b') in self.months) or
                (t[-1].planning_end is not None and
                    t[-1].planning_end.strftime('%b') in self.months) or
                (t[-1].planning_start is not None and t[-1].planning_end is None and
                    t[-1].planning_start <= today)
            ) and
            (
                t[-1].responsible is not None or
                t[-1].prevention_plan is not None or
                t[-1].requirements is not None or
                t[-1].budget is not None or
                t[-1].action_plan is not None
            )
        )]

        modulesdict = defaultdict(lambda: defaultdict(list))
        for module, risk, action in measures:
            if 'custom-risks' not in risk.zodb_path:
                risk_obj = self.request.survey.restrictedTraverse(risk.zodb_path.split('/'))
                title = risk_obj and risk_obj.problem_description or risk.title
            else:
                title = risk.title
            classes = []
            for m in [today, next_month, month_after_next]:
                cls = None
                if action.planning_start:
                    if action.planning_start.month == m.month:
                        cls = "start"
                    if action.planning_end:
                        if action.planning_end.month == m.month:
                            if (
                                action.planning_end.month ==
                                (action.planning_start and action.planning_start.month)
                            ):
                                cls = "start-end"
                            else:
                                cls = "end"
                        elif (
                            action.planning_start.month < m.month and
                            action.planning_end.month > m.month
                        ):
                            cls = "ongoing"
                    elif action.planning_start.month < m.month:
                        cls = "ongoing"

                classes.append(cls)
            modulesdict[module][risk.priority].append(
                {'title': title,
                 'description': action.action_plan,
                 'months': [(action.planning_start and
                            action.planning_start.month == m.month) or
                            (action.planning_end and
                            action.planning_end.month == m.month)
                            for m in [today, next_month, month_after_next]],
                 'classes': classes,
                 })

        # re-use top-level module computation from the Status overview
        modules = self.getModules()
        main_modules = {}
        for module, risks in sorted(modulesdict.items(), key=lambda m: m[0].zodb_path):
            module_obj = self.request.survey.restrictedTraverse(module.zodb_path.split('/'))
            if (
                IProfileQuestion.providedBy(module_obj) or
                ICustomRisksModule.providedBy(module_obj) or
                module.depth >= 3
            ):
                path = module.path[:6]
            else:
                path = module.path[:3]
            if path in main_modules:
                for prio in risks.keys():
                    if prio in main_modules[path]['risks']:
                        main_modules[path]['risks'][prio].extend(risks[prio])
                    else:
                        main_modules[path]['risks'][prio] = risks[prio]
            else:
                title = modules[path]['title']
                number = modules[path]['number']
                main_modules[path] = {'name': title, 'number': number, 'risks': risks}

        self.modules = []
        for key in sorted(main_modules.keys()):
            self.modules.append(main_modules[key])
