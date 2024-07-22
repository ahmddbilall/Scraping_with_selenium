from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 

class linkdin_jobs_scraping(webdriver.Edge):
    
    def __init__(self):
        super(linkdin_jobs_scraping,self).__init__()



    def load_job_page(self,URL):
        '''
        gets the URL of page to be load and wait until the page is loaded
        if page is not loaded in 10 seconds, it will raise an exception
        '''
        self.get(URL)
        self.__wait_for_page_load()
        assert "No results found." not in self.page_source



    def __wait_for_page_load(self):
        '''
        waits for 10 second to load the page 
        if page is not loaded in 10 seconds, it will raise an exception
        '''
        try:
            WebDriverWait(self, 7).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except Exception as e:
            print(f"Error while waiting for page load: {e}")


    def load_Ids_of_all_jobs(self,number_of_pages=20):
        '''
        returns a list of all the IDs of jobs on the page
        '''

        last_height = self.execute_script("return document.body.scrollHeight")    

        jobID = set()
        page = 0
        while True:
            while True:
                li_elements = self.find_elements(By.XPATH, "//ul[@class='scaffold-layout__list-container']/li")
                for li in li_elements:
                    try:
                        job_id = li.get_attribute('data-occludable-job-id')

                        jobID.add(job_id)
                    except Exception as e:
                        print(f"Error processing element: {e}")
                
                
                print("Scrolling...")
                self.execute_script("window.scrollTo(0, document.body.scrollHeight);")    
                time.sleep(5) # pause between scrolls   
                new_height = self.execute_script("return document.body.scrollHeight")


                if new_height == last_height:
                    break
                last_height = new_height
            
            
            
            next_button = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'artdeco-button.artdeco-button--muted.artdeco-button--icon-right.artdeco-button--1.artdeco-button--tertiary.ember-view.jobs-search-pagination__button.jobs-search-pagination__button--next'))
            )
            
            next_button.click()
            page+=1
            if page == number_of_pages:
                print("Reached the last page.")
                break
        return list(jobID)


    def __check_login_page(self):
        try:
            login_button = self.find_element(By.XPATH, '//button[text()=" Agree & Join "]')
            return True
        except Exception:   
            return False


    def Login(self,email,password,login_page_link):
        '''
        logs in to the linkdin account
        '''
        self.get(login_page_link)
        time.sleep(5)
        self.__wait_for_page_load()
        try:
            username_field = self.find_element(By.ID, 'username')
            username_field.send_keys(email)

            password_field = self.find_element(By.ID, 'password')
            password_field.send_keys(password)

            password_field.send_keys(Keys.RETURN)
            time.sleep(5)
            self.__wait_for_page_load()

            if "Feed | LinkedIn" in self.title:
                print("Login successful!")
                return True
            # Wait for verification code input (manually enter the code)
            verification_code = input("Enter the verification code from your email: ")

            code_field = self.find_element(By.ID, 'input__email_verification_pin')
            code_field.send_keys(verification_code)
            code_field.submit()
            self.__wait_for_page_load()

            if "Feed | LinkedIn" in self.title:
                print("Login successful!")
                return True
            else:
                print("Login failed. Check your credentials or other login issues.")
                return False

        except Exception as e:
            print(f"Exception occurred during login: {e}")
            return False
        

    def get_details_of_jobs(self,Ids,Base_link):
        '''
        get a list containing links of linkdin jobs 
        returns a list of dictionaries containing details of each job
        '''
        data = []
        for i,id in enumerate(Ids):
            print(f'getting details of page {i}')
            self.get(Base_link+str(id))

            self.__wait_for_page_load()
            if self.__check_login_page():
                print('login page')
                continue
            dic = {}
            try:
                description_element = self.find_element(By.ID, 'job-details')
                dic['description'] = description_element.text

                company_name_element = self.find_element(By.CLASS_NAME, 'job-details-jobs-unified-top-card__company-name')
                dic['company_name'] = company_name_element.text

                job_title_element = self.find_element(By.CLASS_NAME, 't-24.job-details-jobs-unified-top-card__job-title.job-details-jobs-unified-top-card__job-title--with-margin')
                h1_tag = job_title_element.find_element(By.TAG_NAME, 'h1')
                dic['job_title'] = h1_tag.text

                info = self.find_element(By.CLASS_NAME, 'job-details-jobs-unified-top-card__primary-description-container')
                info = info.text
                info = info.split('·')
                dic['location'] = info[0]
                dic['time_posted'] = info[1]
                dic['applicants'] = info[2]


                type_element = self.find_element(By.CLASS_NAME, 'job-details-jobs-unified-top-card__job-insight.job-details-jobs-unified-top-card__job-insight--highlight')
                dic['type_info'] = type_element.text

                company_info_element = self.find_element(By.CLASS_NAME, 'job-details-jobs-unified-top-card__job-insight')
                dic['company_info'] = company_info_element.text

                skills_elements = self.find_elements(By.CSS_SELECTOR, '.app-aware-link.job-details-how-you-match__skills-item-subtitle.t-14.overflow-hidden')
                if len(skills_elements) >= 2:
                    skills  = skills_elements[0].text 
                    skills  += skills_elements[1].text 
                    dic['skills'] = skills

                data.append(dic)
            except Exception as e:
                print(f"Error: {e}")
                print(f"Error processing job: {id}") 
        return data
        




    # to use this class in with statement    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Closing the browser')
        time.sleep(3)
        self.quit()

    def end(self):
        print('Closing the browser')
        time.sleep(3)
        self.quit()

