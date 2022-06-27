//
//  ViewController.swift
//  AmazSafe
//
//  Created by Kshitij Shrivastava on 30/05/21.
//

import UIKit

class ViewController: UIViewController {

    var funcTimer :Timer?
    
    @IBOutlet weak var alarmStatus: UILabel!
    
    
    @IBOutlet weak var tempStatus: UILabel!
    
    
    @IBOutlet weak var gpsCoordinates: UILabel!
    
    
   
    @IBOutlet weak var OpenTheBoxButton: UIButton!
    
    
    @IBOutlet weak var CloseTheBoxButton: UIButton!
    
    @IBOutlet weak var DeliveryStatusButton: UIButton!
    
    @IBOutlet weak var SanitiseButton: UIButton!
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        
        OpenTheBoxButton.layer.cornerRadius = 20
        CloseTheBoxButton.layer.cornerRadius = 20
        DeliveryStatusButton.layer.cornerRadius = 20
        SanitiseButton.layer.cornerRadius = 20
        let url = "https://io.adafruit.com/api/v2/Shayan2k/feeds/send-esp/data/last?X-AIO-Key=aio_eRXV62PmHE4CDLjJZQh1cW3yPl6X"
        
        funcTimer = Timer.scheduledTimer(timeInterval: 2, target: self, selector: #selector(runTimedCode), userInfo: nil, repeats: true)
        
        
        //getData(from: url)
    }
    
    @objc func runTimedCode(){
        getData(from:"https://io.adafruit.com/api/v2/Shayan2k/feeds/send-esp/data/last?X-AIO-Key=aio_eRXV62PmHE4CDLjJZQh1cW3yPl6X")
    }
    
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        funcTimer?.invalidate()
    }
    func convertToDictionary(text: String) -> [String: Any]? {
        if let data = text.data(using: .utf8) {
            do {
                return try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any]
            } catch {
                print(error.localizedDescription)
            }
        }
        return nil
    }

    func getData(from url:String){
        
        let task = URLSession.shared.dataTask(with: URL(string:url)!, completionHandler:{ data,response,error in

            guard let data = data, error == nil else{
                print("something went wrong")
                return
            }
            
            var result:Response?
            do{
                result = try JSONDecoder().decode(Response.self,from:data)
            }
            catch{
             print("failed to convert \(error.localizedDescription)")
            }
            
            guard let json = result else{
                return
            }
            
            let dict = self.convertToDictionary(text: json.value)
            let dict2:Dictionary = dict!
            let ar:Array = dict2["GPS"]! as! Array<Float>
            var a:String;
            if(dict2["ALARM"] as! Int==0){
            a = "Safe"
            }
            else{
                a = "Threat"
            }
            var temp:Int = dict2["TEMPERATURE"] as! Int
            var s:String = String(ar[0])+" , "+String(ar[1])
            
            DispatchQueue.main.async {
                self.alarmStatus.text = a
                self.tempStatus.text = String(temp)
                self.gpsCoordinates.text = s
                if(a=="Threat"){
                    self.view.backgroundColor = UIColor.red
                }
                    else if(a=="Safe"){
                    self.view.backgroundColor = UIColor.green
            }
            }
        
        })
        
        task.resume()
}
    
    
    
    
    
/*
 {
 "id":"0ER5DQDEH7RE0DM5DKK6PD2XRG",
 "feed_id":1634126,
 "value":"{"IMAGE": null, "GPS": [8, 7], "TEMPERATURE": 4, "ALARM": false}",
 "location":null,
 "created_at":"2021-05-30T08:16:38Z",
 "updated_at":"2021-05-30T08:16:38Z",
 "expiration":"1624954598.0",
 "lat":null,
 "lon":null,
 "ele":null,
 }
 */



struct Response:Codable{
    let id:String
    let feed_id:Int
    let value :String
    let location:String?
    let created_at:String
    let updated_at:String
    let expiration:String
    let lat:String?
    let lon:String?
    let ele:String?
}
/*
struct MyResult:Codable {
    let IMAGE:String?
    let GPS:String
    let TEMPERATURE:Int
    let ALARM:Bool
}
 */

}
