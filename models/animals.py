# -*- coding: utf-8 -*-
from odoo import models, fields, tools, api, _
import time
import odoo.addons.decimal_precision as dp
from time import gmtime, strftime
from odoo.exceptions import Warning, ValidationError
from datetime import datetime,timedelta
from odoo.tools.translate import _

class AnimalsTemplate(models.Model):
    _name = 'animals.template'

# Fonction qui affiche par défaut la date à laquelle le user créer le formulaire
    @api.multi
    def _get_datetime(self):
        date_now = datetime.strftime(datetime.today(), "%Y-%m-%d %H:%M:%S")
        return date_now

# Fonction qui renvoie automatiquement les informations du propriétaire de l'animal
    @api.depends("partner_id")
    def _get_proprietary_data(self):
        partner = self.env['res.partner'].search([('id', '=', self.partner_id.id)])
        if partner.id:
            self.adress = partner.street
            self.city = partner.city
            self.tel = partner.phone
            self.mobile = partner.mobile
            self.email = partner.email

# Ici créer une fonction qui affiche à la séléction du médecin son département, son poste, son supérieur hiérarchique, ...
    @api.depends("employee_id")
    def _get_emp_data(self):
        emp = self.env['hr.employee'].search([('id', '=', self.employee_id.id)])
        if emp.id:
            self.dep_id = emp.department_id
            self.mentor_id = emp.coach_id
            self.poste= emp.job_id
            self.phone = emp.mobile_phone
            self.email_emp = emp.work_email


# Ici ecrire une fonction qui calcule l'age de l'animal et le renvoie dans le champ age
    @api.onchange('born_date', 'consultation_date')
    def _date_error(self):
          if self.born_date>self.consultation_date:
              return { 'warning': 
         { 'title':"Erreur de saisie", 'message':"la date de naisance est incorecte ", }, }
     
    @api.depends('born_date',"consultation_date")
    def _cal_age(self):
        if self.born_date and self.consultation_date:
            t1=datetime.strptime(str(self.born_date),"%Y-%m-%d" )
            t2=datetime.strptime(str(self.consultation_date),"%Y-%m-%d"  )
            d = (t2-t1)/360
            self.age = str(d.days)



# Ici essayer de créer une séquence pour chaque formulaire créer
    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].get('animals.template')
        vals['consultation_num'] = seq
        return super(AnimalsTemplate, self).create(vals)

# workflow and statusbar creation
   
    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'
    def action_done(self):
        for rec in self:
            rec.state = 'done'
    def action_ph(self):
        for rec in self:
            rec.state = 'ph'
    def action_fin(self):
        for rec in self:
            rec.state = 'fin'


    state = fields.Selection([
            ('draft', 'Consultaion'),
            ('confirm', 'Confirmation docteur'),
            ('done', 'Confirmation sup-hier'),
             ('ph', 'Confirmation pharmacien'),
              ('fin', 'Consultation terminer')
        ], string='Status', readonly=True, default='draft')
    consultation_num = fields.Char(string='Numéro de dossier', readonly=True,copy=False)
    consultation_date = fields.Date(u'Date de consultation', default=_get_datetime
                                    , readonly=True)
    name = fields.Char(string=u"Nom animal", required=True,
                        help="Saisissez le nom de votre animal")
    gender = fields.Selection([('mal', 'Male'), ('fem', 'Femelle')]
                             , string=u"Genre")
    type_animals_id = fields.Many2one(string=u"Type animal", comodel_name="animals.type")
    class_animals_id = fields.Many2one(string=u"Classe animal", comodel_name='animals.class')
    milieu_animals_id = fields.Many2one(string=u"Milieu animal", comodel_name='animals_class.milieu')
    born_date = fields.Date(string=u"Date de naissance", required=True)
    age = fields.Integer(string=u"Age" ,compute="_cal_age")

    partner_id = fields.Many2one(string=u"Proprietaire",
                                  comodel_name='res.partner', required=True)
    city = fields.Char(string=u"Ville", compute='_get_proprietary_data', readonly=True)
    adress = fields.Char(string=u"Adresse", compute='_get_proprietary_data', readonly=True)
    tel = fields.Char(string=u"Téléphone", compute='_get_proprietary_data', readonly=True)
    mobile = fields.Char(string=u"Mobile", compute='_get_proprietary_data', readonly=True)
    email = fields.Char(string=u"Email", compute='_get_proprietary_data', readonly=True)

    employee_id = fields.Many2one(string=u"Vétérinaire",
                                    comodel_name='hr.employee', required=True)
    dep_id = fields.Many2one(string=u"departement", compute='_get_emp_data', readonly=True,comodel_name='hr.department')
    mentor_id = fields.Many2one(string=u"superieur hierarechique", compute='_get_emp_data', readonly=True,comodel_name='hr.employee')
    poste = fields.Many2one(string=u"poste occupée", compute='_get_emp_data', readonly=True,comodel_name='hr.job')
    phone = fields.Char(string=u"telephone personnelle", compute='_get_emp_data', readonly=True)
    email_emp = fields.Char(string=u"Email", compute='_get_emp_data', readonly=True)


class TypeAnimals(models.Model):
    _name = 'animals.type'

    name = fields.Char(u"Type animal")

class ClassAnimals(models.Model):
    _name = 'animals.class'

    name = fields.Char(string=u"Classe animal")

class MilieuAnimals(models.Model):
    _name = 'animals_class.milieu'

    name = fields.Char(u"Milieu")
